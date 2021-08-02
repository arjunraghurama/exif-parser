import streamlit as st
from PIL import Image, ExifTags
import requests
from streamlit.errors import Error

st.set_page_config(
        page_title="Exif Data Parser",
        page_icon="🌟",
        layout="centered"
    )

# For parsing exif data from an image
def parse_exif(file) -> str:
    data = Image.open(file)
    exif = data.getexif()
    json_data = {}
    count = 0
    for key, val in exif.items():
        if key in ExifTags.TAGS:
            json_data[count] = { "TagName" : ExifTags.TAGS[key],
                                 "TagKey" : key,
                                 "TagValue" : val }
            count+=1
    return json_data

def print_json_data(json_data):
    if len(json_data) > 0:
            st.json(json_data)
    else:
        msg = "No Tags found in given Image 😞"
        st.markdown("""<p><span align="center">{}</span></p>""".format(msg),unsafe_allow_html=True)

def main():
    try:
        st.title("Parse image for EXIF Tags")
        st.empty()
        st.write("EXIF is short for Exchangeable Image File, a format that is a standard for storing interchange information in digital photography image files using JPEG compression. Almost all new digital cameras use the EXIF annotation, storing information on the image such as shutter speed, exposure compensation, F number, what metering system was used, if a flash was used, ISO number, date and time the image was taken, whitebalance, auxiliary lenses that were used and resolution. Some images may even store GPS information so you can easily see where the images were taken")
        files = st.file_uploader("Upload file",accept_multiple_files=True)
        st.write("OR")
        url = st.text_input("Image URL")
        json_data = {}
        #  For uploaded files
        if len(files)>0:
            for file in files:
                json_data = parse_exif(file)
                st.write("File : "+ file.name)
                print_json_data(json_data) 

        #  For input url of image
        if url:
            image = requests.get(url, stream=True).raw
            print(image.__str__())
            json_data = parse_exif(image)
            print_json_data(json_data)
        

    except Error as err:
        er = "404 Oh Snap!! We are unable to parse the image 😞"
        st.markdown(""" <p><span align="center">{}</span></p>""".format(er),unsafe_allow_html=True)



if __name__ == "__main__":
    main()

footer="""<style>
a:link , a:visited{
color: #ecedf3;
background-color: transparent;
text-decoration: underline;
}
a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}
.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: black;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p style='color: #ecedf3;'> Made with <a style="text-decoration:none" href="https://streamlit.io/" target="blank"> Streamlit </a>❤  <a> by</a><a style='display: block; text-align: center; text-decoration:none;' href="https://github.com/arjunraghurama" target="blank">Arjun</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
