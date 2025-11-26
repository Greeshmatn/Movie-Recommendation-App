import streamlit as st
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import base64

if "movie_dict" not in st.session_state:
    with open("movie_dict.pkl", "rb") as obj1:
        movie = pickle.load(obj1)
    st.session_state["movie_dict"] = movie

def recommend_movies(movie_name, n):
    movie_dictionary = st.session_state["movie_dict"]
    if movie_name in movie_dictionary:
        movie_vector = movie_dictionary[movie_name]
        cosine_values = {}
        for movie, vector in movie_dictionary.items():
            if movie != movie_name:
                cosine_values[movie] = cosine_similarity([vector], [movie_vector])[0][0]
        return list(dict(sorted(cosine_values.items(), key = lambda x:x[1], reverse=True)[:n]))
    else:
        return None


def get_base64(img_path):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_base64 = get_base64("Elements of cinema dark.jpg")

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpg;base64,{img_base64}");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
}}
</style>
""", unsafe_allow_html=True)

df = pd.read_csv("imdb_top_1000.csv")
# st.title("Movie Recommendation App")
st.markdown("<p style='color:brown; font-size:50px; \
    font-weight:bold;'>Movie Recommendation App</p>", unsafe_allow_html=True)
st.markdown("<h3 style='color:white;'>Select a Movie</h3>", unsafe_allow_html=True)
movie = st.selectbox("", st.session_state["movie_dict"].keys())
button = st.button("Recommend")
col1, col2 = st.columns([1,1])  # To split the screen to 2 equal parts. [3,1] will give more space for 1st col and less for 2nd col. [1,1,1] will divide equally for 3 columns.

def get_high_quality_image(url, width=600, height=900):
    if "UX" in url:
        url = url.replace("UX67", f"UX{width}")
    if "UY" in url:
        url = url.replace("UY98", f"UY{900}")  
    
    if "CR" in url:
        url = url.replace("CR0,0,67,98", f"CR0,0,{width},{height}")
        url = url.replace("CR2,0,67,98", f"CR2,0,{900},{1200}")

    return url

if button:
    def movie_block(title, director, star1, star2, released_yr, genre, certificate, imdb_rating, poster_link):
        st.markdown(f"""
        <div style="padding:10px; border-bottom:1px solid #ddd;">
            <h3 style="margin-bottom:5px;">{title}</h3>
            <img src="{get_high_quality_image(poster_link)}" width="150">
            <br/>
            <table style="width:100%; border-collapse: collapse;">
                <tr>
                    <td style="width:30%; font-weight:bold;">Director</td>
                    <td>{director}</td>
                </tr>
                <tr>
                    <td style="font-weight:bold;">Starring</td>
                    <td>{star1}, {star2}</td>
                </tr>
                <tr>
                    <td style="font-weight:bold;">Released Year</td>
                    <td>{released_yr}</td>
                </tr>
                <tr>
                    <td style="font-weight:bold;">Genre</td>
                    <td>{genre}</td>
                </tr>
                <tr>
                    <td style="font-weight:bold;">Certificate</td>
                    <td>{certificate}</td>
                </tr>
                <tr>
                    <td style="font-weight:bold;">IMDB Rating</td>
                    <td>{imdb_rating}</td>
                </tr>
            </table>
            <br>
        </div>
        """, unsafe_allow_html=True)     



    res = recommend_movies(movie_name=movie, n=6)

    with col1:
        for i in res[:3]:
            movie_block(
                title = i,
                director = df.loc[df["Series_Title"] == i, "Director"].iloc[0],
                star1 = df.loc[df["Series_Title"] == i, "Star1"].iloc[0],
                star2 = df.loc[df["Series_Title"] == i, "Star2"].iloc[0],
                released_yr = df.loc[df["Series_Title"] == i, "Released_Year"].iloc[0],
                genre = df.loc[df["Series_Title"] == i, "Genre"].iloc[0],
                certificate = df.loc[df["Series_Title"] == i, "Certificate"].iloc[0],
                imdb_rating = df.loc[df["Series_Title"] == i, "IMDB_Rating"].iloc[0],
                poster_link = df.loc[df["Series_Title"] == i, "Poster_Link"].iloc[0],
            )

    with col2:
        for i in res[3:]:
            movie_block(
                title = i,
                director = df.loc[df["Series_Title"] == i, "Director"].iloc[0],
                star1 = df.loc[df["Series_Title"] == i, "Star1"].iloc[0],
                star2 = df.loc[df["Series_Title"] == i, "Star2"].iloc[0],
                released_yr = df.loc[df["Series_Title"] == i, "Released_Year"].iloc[0],
                genre = df.loc[df["Series_Title"] == i, "Genre"].iloc[0],
                certificate = df.loc[df["Series_Title"] == i, "Certificate"].iloc[0],
                imdb_rating = df.loc[df["Series_Title"] == i, "IMDB_Rating"].iloc[0],
                poster_link = df.loc[df["Series_Title"] == i, "Poster_Link"].iloc[0],
            )

    # with col1:
    #     for i in res[:3]:
    #         st.subheader(f"Series Title: {i}")
    #         director = df.loc[df["Series_Title"] == i, "Director"].iloc[0]
    #         st.write(f"Director: {director}")
    #         star1 = df.loc[df["Series_Title"] == i, "Star1"].iloc[0]
    #         star2 = df.loc[df["Series_Title"] == i, "Star2"].iloc[0]
    #         st.write(f"Starring: {star1}, {star2}")
    #         released_yr = df.loc[df["Series_Title"] == i, "Released_Year"].iloc[0]
    #         st.write(f"Released Year: {released_yr}")
    #         genre = df.loc[df["Series_Title"] == i, "Genre"].iloc[0]
    #         st.write(f"Genre: {genre}")
    #         link = df.loc[df["Series_Title"] == i, "Poster_Link"].iloc[0]
    #         st.image(get_high_quality_image(link), 100, 100)
    #         st.write("_"*1000)
    # with col2:
    #     for i in res[3:]:
    #         st.subheader(f"Series Title: {i}")
    #         director = df.loc[df["Series_Title"] == i, "Director"].iloc[0]
    #         st.write(f"Director: {director}")
    #         star1 = df.loc[df["Series_Title"] == i, "Star1"].iloc[0]
    #         star2 = df.loc[df["Series_Title"] == i, "Star2"].iloc[0]
    #         st.write(f"Starring: {star1}, {star2}")
    #         released_yr = df.loc[df["Series_Title"] == i, "Released_Year"].iloc[0]
    #         st.write(f"Released Year: {released_yr}")
    #         genre = df.loc[df["Series_Title"] == i, "Genre"].iloc[0]
    #         st.write(f"Genre: {genre}")
    #         link = df.loc[df["Series_Title"] == i, "Poster_Link"].iloc[0]
    #         st.image(get_high_quality_image(link), 100, 100)
    #         st.write("_"*1000)