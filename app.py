import streamlit as st
# NLP Pkgs
from textblob import TextBlob
import pandas as pd
# Emoji
import emoji

# Web Scraping Pkg
from bs4 import BeautifulSoup
from urllib.request import urlopen

# Fetch Text From Url
@st.cache
def get_text(raw_url):
    page = urlopen(raw_url)
    soup = BeautifulSoup(page, 'html.parser')
    fetched_text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return fetched_text


def main():
    """Sentiment Analysis Web App """

    st.title("Sentiment Analyzer Web App")
    st.subheader("made with Streamlit")

    activities = ["Sentiment Analysis", "Text Analysis on URL", "About"]
    select = st.selectbox("Choose", activities)

    if select == 'Sentiment Analysis':
        st.subheader("Sentiment Analysis")
        st.write(emoji.emojize('Hello there :red_heart:', use_aliases=True))
        raw_text = st.text_area("Enter Your Text", "Type Here")
        if st.button("Analyze"):
            blob = TextBlob(raw_text)
            result = blob.sentiment.polarity
            if result > 0.0:
                custom_emoji = ':smile: Happy'
                st.write(emoji.emojize(custom_emoji, use_aliases=True))
            elif result < 0.0:
                custom_emoji = ':disappointed: Sad/Disappointed'
                st.write(emoji.emojize(custom_emoji, use_aliases=True))
            else:
                st.write(emoji.emojize(':expressionless: Expressionless', use_aliases=True))
            st.info("Polarity Score is = {}".format(result))

    if select == 'Text Analysis on URL':
        st.subheader("Analysis on Text From URL")
        raw_url = st.text_input("Enter URL Here", "Enter here (URL Only)")
        text_preview_length = st.slider("Length to Preview", 1, 100)

        if st.button("Analyze"):
            my_bar = st.progress(0)

            my_bar.progress(10)
            if raw_url != "Enter here (URL Only)":
                result = get_text(raw_url)
                blob = TextBlob(result)
                len_of_full_text = len(result)
                my_bar.progress(20)
                len_of_short_text = round(len(result) / text_preview_length)
                st.success("Length of Full Text {}".format(len_of_full_text))
                st.success("Length of Short Text {}".format(len_of_short_text))
                st.info(result[:len_of_short_text])
                my_bar.progress(50 + 1)
                c_sentences = [sent for sent in blob.sentences]
                c_sentiment = [sent.sentiment.polarity for sent in blob.sentences]
                #st.write(len(c_sentiment))
                emoji_lst = []
                for i in range(len(c_sentiment)):
                    if c_sentiment[i] > 0.00:
                        emoji_lst.append(emoji.emojize(':smile: Smile', use_aliases=True))
                    elif c_sentiment[i] < 0.00:
                        emoji_lst.append(emoji.emojize(':disappointed:', use_aliases=True))
                    else:
                        emoji_lst.append("No expression")

                new_df = pd.DataFrame(zip(c_sentences, c_sentiment, emoji_lst), columns=['Sentence', 'Sentiment', "Emoji"])
                st.dataframe(new_df)
                my_bar.progress(100)



    if select == 'About':
        st.subheader("Sentiment Analyzer Web App with streamlit, emoji, textblob")
        st.info("mazqoty.01@gmail.com")


if __name__ == '__main__':
    main()
