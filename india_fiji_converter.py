"""
India -> Fiji (Suva) time converter for Streamlit apps.

Integration in your MOA Extractor app:
    from india_fiji_converter import render_india_fiji_converter

Then call this where you want the converter to appear:
    render_india_fiji_converter()

Uses Python's built-in zoneinfo. Fiji daylight-saving changes (when applicable)
are handled automatically by the Pacific/Fiji timezone database.
"""

from datetime import datetime, date, time
from zoneinfo import ZoneInfo

import streamlit as st


INDIA_TZ = ZoneInfo("Asia/Kolkata")
FIJI_TZ = ZoneInfo("Pacific/Fiji")


def _current_india_datetime():
    return datetime.now(INDIA_TZ)


def _format_date(value: date) -> str:
    return value.strftime("%A, %d %B %Y")


def render_india_fiji_converter():
    """Render a compact India-to-Suva converter in the current Streamlit page."""

    now_india = _current_india_datetime()

    st.markdown(
        """
        <style>
        .ifc-wrap {
            background: linear-gradient(135deg, #111d35, #1c3b5c);
            border: 1px solid #345477;
            border-radius: 16px;
            padding: 20px 22px;
            margin: 8px 0 18px 0;
            color: #f8fafc;
        }
        .ifc-kicker {
            color: #a8c8e8;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: .16em;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        .ifc-title {
            color: white;
            font-size: 21px;
            font-weight: 800;
            margin-bottom: 3px;
        }
        .ifc-subtitle {
            color: #bfd0e3;
            font-size: 12px;
            margin-bottom: 15px;
        }
        .ifc-result {
            background: rgba(255,255,255,.08);
            border: 1px solid rgba(191,219,254,.22);
            border-radius: 12px;
            padding: 15px 17px;
            margin-top: 8px;
        }
        .ifc-result-label {
            color: #b9dafa;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: .13em;
        }
        .ifc-result-time {
            color: #fff;
            font-size: clamp(28px, 4vw, 39px);
            line-height: 1.2;
            font-weight: 800;
            margin-top: 5px;
        }
        .ifc-result-date {
            color: #d7e8fa;
            font-size: 14px;
            margin-top: 3px;
        }
        .ifc-note {
            color: #b7c8da;
            font-size: 11px;
            margin-top: 12px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if "ifc_india_date" not in st.session_state:
        st.session_state.ifc_india_date = now_india.date()
    if "ifc_india_time" not in st.session_state:
        st.session_state.ifc_india_time = now_india.time().replace(second=0, microsecond=0)

    st.markdown(
        """
        <div class="ifc-wrap">
          <div class="ifc-kicker">World clock · Time converter</div>
          <div class="ifc-title">🇮🇳 India → 🇫🇯 Fiji · Suva</div>
          <div class="ifc-subtitle">Choose an India date and time to calculate the matching Suva date and time.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_date, col_time = st.columns(2)
    with col_date:
        india_date = st.date_input(
            "India date",
            key="ifc_india_date",
            format="DD/MM/YYYY",
        )
    with col_time:
        india_time = st.time_input(
            "India time",
            key="ifc_india_time",
            step=60,
        )

    if st.button("Use current India date & time", key="ifc_use_now", use_container_width=True):
        current = _current_india_datetime()
        st.session_state.ifc_india_date = current.date()
        st.session_state.ifc_india_time = current.time().replace(second=0, microsecond=0)
        st.rerun()

    # Interpret the selected wall-clock value in India, then convert the
    # same instant to Suva. ZoneInfo applies the correct Fiji UTC offset.
    india_datetime = datetime.combine(india_date, india_time).replace(tzinfo=INDIA_TZ)
    fiji_datetime = india_datetime.astimezone(FIJI_TZ)

    # Calculate the actual offset difference for the selected date.
    difference = fiji_datetime.utcoffset() - india_datetime.utcoffset()
    total_minutes = int(difference.total_seconds() // 60)
    sign = "ahead of" if total_minutes >= 0 else "behind"
    abs_minutes = abs(total_minutes)
    hours, minutes = divmod(abs_minutes, 60)
    difference_text = f"Fiji is {hours}h {minutes:02d}m {sign} India"

    st.markdown(
        f"""
        <div class="ifc-result">
          <div class="ifc-result-label">🇫🇯 FIJI · SUVA LOCAL TIME</div>
          <div class="ifc-result-time">{fiji_datetime.strftime("%I:%M %p").lstrip("0")}</div>
          <div class="ifc-result-date">{_format_date(fiji_datetime.date())}</div>
          <div class="ifc-note">{difference_text} · Time zone: Pacific/Fiji</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    return fiji_datetime
