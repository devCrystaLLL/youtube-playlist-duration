import requests
import streamlit as st
# from streamlit_lottie import st_lottie
from PIL import Image
from yt_playlist_duration import YtPlaylistDuration
import util.Duration as duration

# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Youtube Playlist Duration Calculator", page_icon=":🏳️‍🌈:", layout="wide")


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def write_playlist_not_valid_error():
    st.markdown(not_valid_playlist_text, unsafe_allow_html=True)


def print_playlist_details(playlist):
    hours = str(playlist.playlist_duration.hours)
    minutes = str(playlist.playlist_duration.minutes)
    seconds = str(playlist.playlist_duration.seconds)

    average_video_hours = str(playlist.average_video_duration.hours)
    average_video_minutes = str(playlist.average_video_duration.minutes)
    average_video_seconds = str(playlist.average_video_duration.seconds)

    playlist_duration_at_1_point_25x_in_secs = playlist.playlist_duration.total_seconds / 1.25
    playlist_duration_at_1_point_5x_in_secs = playlist.playlist_duration.total_seconds / 1.5
    playlist_duration_at_1_point_75x_in_secs = playlist.playlist_duration.total_seconds / 1.75
    playlist_duration_at_2x_in_secs = playlist.playlist_duration.total_seconds / 2

    playlist_duration_at_1_point_25x = \
        duration.convert_from_seconds_to_duration(playlist_duration_at_1_point_25x_in_secs)
    playlist_duration_at_1_point_5x = \
        duration.convert_from_seconds_to_duration(playlist_duration_at_1_point_5x_in_secs)
    playlist_duration_at_1_point_75x = \
        duration.convert_from_seconds_to_duration(playlist_duration_at_1_point_75x_in_secs)
    playlist_duration_at_2x = \
        duration.convert_from_seconds_to_duration(playlist_duration_at_2x_in_secs)

    number_of_videos = str(playlist.number_of_videos)

    st.write(" ")

    category_column, first_column, minutes_column, seconds_column, ignored_1, ignored_2, ignored_3 = \
        st.columns([0.9, 0.5, 0.5, 0.5, 1.5, 1.5, 1.5])

    with category_column:
        st.write("Playlist Duration:")
        st.write("No. of Videos:")
        st.write("Average Video Duration:")

        st.write("⠀")

        st.write(f"Playlist Duration at 1.25x:")
        st.write(f"Playlist Duration at 1.5x:")
        st.write(f"Playlist Duration at 1.75x:")
        st.write(f"Playlist Duration at 2x:")

    with first_column:
        st.write(f"Hours: {hours}")
        st.write(number_of_videos)
        st.write(f"Hours: {average_video_hours}")

        st.write("⠀")

        st.write(f"Hours: {playlist_duration_at_1_point_25x.hours}")
        st.write(f"Hours: {playlist_duration_at_1_point_5x.hours}")
        st.write(f"Hours: {playlist_duration_at_1_point_75x.hours}")
        st.write(f"Hours: {playlist_duration_at_2x.hours}")

    with minutes_column:
        st.write(f"Minutes: {minutes}")
        st.write("⠀")
        st.write(f"Minutes: {average_video_minutes}")

        st.write("⠀")

        st.write(f"Minutes: {playlist_duration_at_1_point_25x.minutes}")
        st.write(f"Minutes: {playlist_duration_at_1_point_5x.minutes}")
        st.write(f"Minutes: {playlist_duration_at_1_point_75x.minutes}")
        st.write(f"Minutes: {playlist_duration_at_2x.minutes}")

    with seconds_column:
        st.write(f"Seconds: {seconds}")
        st.write("⠀")
        st.write(f"Seconds: {average_video_seconds}")

        st.write("⠀")

        st.write(f"Seconds: {playlist_duration_at_1_point_25x.seconds}")
        st.write(f"Seconds: {playlist_duration_at_1_point_5x.seconds}")
        st.write(f"Seconds: {playlist_duration_at_1_point_75x.seconds}")
        st.write(f"Seconds: {playlist_duration_at_2x.seconds}")

    st.write("##")
    st.write("##")


local_css("style/style.css")

# ---- LOAD ASSETS ----
lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
img_contact_form = Image.open("images/yt_contact_form.png")
img_lottie_animation = Image.open("images/yt_lottie_animation.png")

YtPlaylistDuration.__init__(YtPlaylistDuration, "AIzaSyADfggwBl8GReXvOJnNdImIXL52s8YUV9o")

not_valid_playlist_text = """<span style='color: red;'>Playlist is invalid.</span>"""

# ---- HEADER SECTION ----
with st.container():
    st.subheader("Hi, I am _CrystaLLL :wave:")
    st.title("A Professional Dumbass")
    st.write(
        # "I am passionate about finding ways to use Python and VBA to be more efficient and effective in business settings."
        "Java go brrrrrrrr"
    )
    st.write("[Learn More](https://www.merriam-webster.com/dictionary/dumbass)")

# ---- TITLE ----
with st.container():
    st.write("---")

    middle_column = st.columns(3)[1]
    with middle_column:
        st.header("Youtube Playlist Duration")

# ---- PLAYLIST DURATION CALCULATOR ----

with st.container():
    playlist_url = st.text_input("Playlist URL", placeholder="Playlist URL", label_visibility='hidden')

    if len(playlist_url) > 0:
        if playlist_url.__contains__("https://www.youtube.com/watch?v="):
            playlist = YtPlaylistDuration.get_playlist_by_url(YtPlaylistDuration, playlist_url)

            if playlist.isValid:
                print_playlist_details(playlist)
            else:
                write_playlist_not_valid_error()
        else:
            write_playlist_not_valid_error()

# ---- CONTACT ----
with st.container():
    st.write("---")
    st.header("Get In Touch With Me!")

    # Documention: https://formsubmit.co/ !!! CHANGE EMAIL ADDRESS !!!
    contact_form = """
    <form action="https://formsubmit.co/send.feedback.net@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here" required></textarea>
        <button type="submit">Send</button>
    </form>
    """
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown(contact_form, unsafe_allow_html=True)
    with right_column:
        st.empty()

st.write("B.S I know this is slow, but please, wait until it says 'Thank You'")
