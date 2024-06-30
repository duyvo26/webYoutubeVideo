import streamlit as st
from html_ import get_html_from_url, extract_text_from_xpath
from streamlit_js_eval import streamlit_js_eval


def loadVideo(url):
    id = url.replace("https://www.youtube.com/watch?v=", "")
    html = f"""
    <iframe allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen="" frameborder="0" referrerpolicy="strict-origin-when-cross-origin" src="https://www.youtube-nocookie.com/embed/{id}?si=HiPKZB_iyPiLh11m&amp;start=3" title="YouTube video player" width="100%">
    """
    st.markdown(html, unsafe_allow_html=True)


title = st.text_input("Nội dung tìm kiếm", "")
if st.button("Tìm kiếm 🔍"):
    target_url = f"https://www.google.com/search?q={title}&tbm=vid"
    html_content = get_html_from_url(target_url)
    video_links = extract_text_from_xpath(html_content)

    html_string = "<hr><h3>Danh sách video</h3>"
    st.markdown(html_string, unsafe_allow_html=True)

    for index, val in enumerate(video_links):
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