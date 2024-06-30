import streamlit as st
from html_ import get_html_from_url, extract_text_from_xpath
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(
    # page_title="Ex-stream-ly Cool App",
    # page_icon="🧊",
    layout="wide",
    # menu_items={
    # },
)

try:
    width = streamlit_js_eval(js_expressions="screen.width", key="SCR")
    height = width * 0.4
    if width < 700:
        height = width * 0.6
except:  # noqa: E722
    pass


def loadVideo(url):
    if "title" in st.session_state:
        with st.sidebar:
            title = st.text_input("Nội dung tìm kiếm", "", key="002")
            if st.button("Tìm kiếm 🔍", key="Btn002"):
                with st.spinner("Đang tìm kiếm video xin chờ..."):
                    loadViewVideo(title)
            loadArrVideo()

    id = url.replace("https://www.youtube.com/watch?v=", "")
    html = f"""
    <iframe height={height} allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen="" frameborder="0" referrerpolicy="strict-origin-when-cross-origin" src="https://www.youtube-nocookie.com/embed/{id}?si=HiPKZB_iyPiLh11m&amp;start=3" title="YouTube video player" width="100%">
    """
    st.markdown(html, unsafe_allow_html=True)


def loadViewVideo(title):
    st.session_state.title = title

    target_url = f"https://www.google.com/search?q={title}&tbm=vid"
    html_content = get_html_from_url(target_url)
    st.session_state.video_links = extract_text_from_xpath(html_content)

def loadArrVideo():
    html_string = "<h3>Danh sách video</h3>"
    st.markdown(html_string, unsafe_allow_html=True)

    for index, val in enumerate(st.session_state.video_links):
        if val[2] is not None:
            st.image(val[2], use_column_width="auto")
            st.write(val[1])
            st.button(
                "xem video 🎞️",
                key=index,
                args=(f"{val[0]}",),
                on_click=loadVideo,
                kwargs=None,
                disabled=False,
                type="primary",
            )


titleView = st.empty()
buttonView = st.empty()
title = titleView.text_input("Nội dung tìm kiếm", "", key="001")
if buttonView.button("Tìm kiếm 🔍", key="Btn001"):
    titleView.empty()
    buttonView.empty()
    with st.spinner("Đang tìm kiếm video xin chờ..."):
        loadViewVideo(title)
        loadArrVideo()