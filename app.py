import csv
import io
import time
import webbrowser

import pandas as pd
import streamlit as st

from extract_links import extract_profile_urls


CSV_COLUMNS = ["linkedin_url", "status", "note"]
STATUS_OPTIONS = ["pending", "opened", "connected", "skipped"]
DEFAULT_CSV_FILE = "linkedin_profiles.csv"


def build_profiles_dataframe(links):
    return pd.DataFrame(
        [{"linkedin_url": link, "status": "pending", "note": ""} for link in links],
        columns=CSV_COLUMNS,
    )


def dataframe_to_csv_bytes(dataframe):
    return dataframe.to_csv(index=False).encode("utf-8")


def read_uploaded_csv(uploaded_file):
    text = uploaded_file.getvalue().decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    rows = list(reader)
    missing_columns = [column for column in CSV_COLUMNS if column not in (reader.fieldnames or [])]
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"CSV is missing required columns: {missing}")
    return pd.DataFrame(rows, columns=CSV_COLUMNS)


def save_profiles_csv(dataframe, output_file=DEFAULT_CSV_FILE):
    dataframe.to_csv(output_file, index=False)


def open_profiles(dataframe, status_filter, limit, interval):
    matching_indexes = dataframe.index[dataframe["status"].isin(status_filter)].tolist()
    selected_indexes = matching_indexes[:limit]

    progress = st.progress(0)
    status_line = st.empty()

    for position, index in enumerate(selected_indexes, start=1):
        url = dataframe.at[index, "linkedin_url"]
        status_line.write(f"Opening {position}/{len(selected_indexes)}: {url}")
        webbrowser.open(url)
        dataframe.at[index, "status"] = "opened"
        progress.progress(position / len(selected_indexes))

        if position < len(selected_indexes):
            time.sleep(interval)

    status_line.write(f"Opened {len(selected_indexes)} profiles.")
    return dataframe, len(selected_indexes)


def render_usage_warning():
    st.warning(
        "This app only opens profile pages. Keep connection requests manual and personalized. "
        "LinkedIn does not publish a fixed daily personal connection limit; official help says "
        "accounts can be restricted after sending many invitations in a short time, receiving too "
        "many ignored/spam-marked invites, or using automation tools."
    )
    st.caption(
        "Helpful references: "
        "[Types of restrictions for sending invitations]"
        "(https://www.linkedin.com/help/linkedin/answer/a551012/types-of-restrictions-for-sending-invitations), "
        "[Invitation limit reached]"
        "(https://www.linkedin.com/help/lms/answer/a550555), "
        "[Network size limit]"
        "(https://www.linkedin.com/help/linkedin/answer/a567364)."
    )


def init_state():
    if "profiles_df" not in st.session_state:
        st.session_state.profiles_df = pd.DataFrame(columns=CSV_COLUMNS)


def main():
    st.set_page_config(
        page_title="WhatsApp to LinkedIn Connector",
        page_icon="in",
        layout="wide",
    )
    init_state()

    st.title("WhatsApp to LinkedIn Connector")
    st.caption("Extract LinkedIn profile URLs from WhatsApp exports and manage a safer manual networking workflow.")

    with st.sidebar:
        st.header("Import")
        chat_file = st.file_uploader("Drop WhatsApp chat .txt", type=["txt"])
        csv_file = st.file_uploader("Or resume from profiles CSV", type=["csv"])

        if chat_file:
            text = chat_file.getvalue().decode("utf-8", errors="replace")
            links = extract_profile_urls(text)
            st.session_state.profiles_df = build_profiles_dataframe(links)
            st.success(f"Extracted {len(links)} unique profiles.")

        if csv_file:
            try:
                st.session_state.profiles_df = read_uploaded_csv(csv_file)
                st.success(f"Loaded {len(st.session_state.profiles_df)} profiles from CSV.")
            except ValueError as error:
                st.error(str(error))

        st.divider()
        st.header("Export")
        st.download_button(
            "Download CSV",
            dataframe_to_csv_bytes(st.session_state.profiles_df),
            file_name=DEFAULT_CSV_FILE,
            mime="text/csv",
            disabled=st.session_state.profiles_df.empty,
        )

        if st.button("Save CSV locally", disabled=st.session_state.profiles_df.empty):
            save_profiles_csv(st.session_state.profiles_df)
            st.success(f"Saved {DEFAULT_CSV_FILE}")

    profiles_df = st.session_state.profiles_df.copy()

    total_profiles = len(profiles_df)
    pending_count = int((profiles_df["status"] == "pending").sum()) if total_profiles else 0
    opened_count = int((profiles_df["status"] == "opened").sum()) if total_profiles else 0
    connected_count = int((profiles_df["status"] == "connected").sum()) if total_profiles else 0
    skipped_count = int((profiles_df["status"] == "skipped").sum()) if total_profiles else 0

    metric_columns = st.columns(4)
    metric_columns[0].metric("Profiles", total_profiles)
    metric_columns[1].metric("Pending", pending_count)
    metric_columns[2].metric("Opened", opened_count)
    metric_columns[3].metric("Connected", connected_count)

    tab_profiles, tab_open, tab_notes = st.tabs(["Profiles", "Open Queue", "Ideas"])

    with tab_profiles:
        st.subheader("Tracking Sheet")
        if profiles_df.empty:
            st.info("Drop a WhatsApp chat export or upload an existing CSV to begin.")
        else:
            edited_df = st.data_editor(
                profiles_df,
                hide_index=True,
                use_container_width=True,
                num_rows="dynamic",
                column_config={
                    "linkedin_url": st.column_config.LinkColumn("LinkedIn URL"),
                    "status": st.column_config.SelectboxColumn("Status", options=STATUS_OPTIONS),
                    "note": st.column_config.TextColumn("Note"),
                },
            )
            st.session_state.profiles_df = edited_df

    with tab_open:
        st.subheader("Profile Opening Controls")
        render_usage_warning()

        open_enabled = st.checkbox("Open profile pages automatically in my local browser")
        control_columns = st.columns(3)
        with control_columns[0]:
            status_filter = st.multiselect(
                "Open rows with status",
                STATUS_OPTIONS,
                default=["pending"],
            )
        with control_columns[1]:
            interval = st.slider("Interval between profiles", 5, 60, 12, help="Seconds")
        with control_columns[2]:
            filtered_count = (
                int(profiles_df["status"].isin(status_filter).sum())
                if total_profiles and status_filter
                else 0
            )
            max_limit = max(1, filtered_count or total_profiles or 1)
            limit = st.number_input("Profiles to open", 1, max_limit, min(10, max_limit))

        st.caption(
            f"{filtered_count} profiles match the current filter. Suggested practice: open a small batch, review each profile, send thoughtful requests manually, "
            "then mark rows as connected or skipped."
        )

        if st.button("Start Opening Queue", disabled=profiles_df.empty or not open_enabled):
            if not status_filter:
                st.error("Choose at least one status filter.")
            else:
                updated_df, opened_total = open_profiles(
                    st.session_state.profiles_df.copy(),
                    status_filter,
                    int(limit),
                    int(interval),
                )
                st.session_state.profiles_df = updated_df
                st.success(f"Opened {opened_total} profiles and marked them as opened.")

    with tab_notes:
        st.subheader("Feature Branch Ideas")
        st.markdown(
            """
- Batch presets: light networking, event follow-up, and deep review modes.
- Duplicate insights: show repeated links and which chat lines mentioned them.
- Contact outcome tracker: pending, opened, connected, replied, follow-up later, skipped.
- CSV merge: upload an older tracking sheet and merge new profiles without losing notes.
- Personalized note drafts: generate short note templates from manually entered context.
- Daily session log: count opened profiles per day so you can pace outreach.
- Search and filters: filter by status, keywords in notes, or URL slug.
- Safer browser mode: open one profile at a time with a next button instead of timed batches.
            """.strip()
        )

    if skipped_count:
        st.caption(f"{skipped_count} profiles are currently marked skipped.")


if __name__ == "__main__":
    main()
