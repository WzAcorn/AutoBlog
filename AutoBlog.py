import logging
import requests
from bs4 import BeautifulSoup
import openai
import json
import time
import TistoryAPI as tistory

# OpenAI API 키 설정
openai.api_key = "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"

#Tistory API설정.
access_token = "5d692352dbcea2d43384a81c7f459de1_0590de3c23fcadafa068dfcb97ff68b4"
redirect_uri = "https://wzacorn.tistory.com/"

def reformat_content_for_blog(text, title):
    try:
        instruction = (
            f"You are a top-notch blogger with super high profits."
            f"Please write the content being recreated in Korean. and write the post start Title:'{title}' in 1 sentence."
            f"Rewrite the following news article for a blog post. Make it engaging, Plain"
            f"comments or opinions to make it more appealing. Title: {title}, Article: {text}"
        )
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",  # Specify the chat model here
            messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": f"Title: {title}, Article: {text}"}
            ]
        )
        reformatted_content = response.choices[0].message['content'].strip()
        logging.info("reformat_content_for_blog 성공",reformatted_content)
        return reformatted_content
    except Exception as e:
        logging.info(f"reformat_content_for_blog 오류 발생: {e}")
        return ""

def get_html_tag(text):
    try:
        instruction = (
            f"Split the paragraphs of the article and add html tags"
            f"Please don't reply other than adding tags."
        )
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",  # Specify the chat model here
            messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": f"{text}"}
            ]
        )
        content = response.choices[0].message['content'].strip()
        logging.info("get_html_tag 성공:",content)
        return content
    except Exception as e:
        logging.error(f"get_html_tag 오류 발생: {e}")
        return ""
        


# AI Times 웹사이트 URL


def get_article_content(article_url):
    # 기사 URL에서 HTML 콘텐츠를 가져옴
    response = requests.get(article_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 기사의 본문을 찾음
    article_body = soup.find('article', {'id': 'article-view-content-div'})
    if not article_body:
        return 'No content found'

    # 본문의 모든 <p> 태그에서 텍스트를 추출
    paragraphs = article_body.find_all('p')
    contents = ' '.join([para.get_text().strip() for para in paragraphs])
    
    return contents

def extract_title_and_content(blog_contents):
    # Title 태그를 찾고 그 위치를 확인
    title_start = blog_contents.find("Title: ")
    if title_start == -1:
        return "제목을 찾을 수 없습니다.", ""

    # Title 태그 다음부터 줄바꿈 문자까지가 제목
    title_end = blog_contents.find("\n", title_start)
    if title_end == -1:
        title_end = len(blog_contents)

    # 제목과 내용 추출
    blog_title = blog_contents[title_start + len("Title: "):title_end].strip()
    blog_content = blog_contents[title_end:].strip()

    return blog_title, blog_content


def get_top_articles(url):
    # 웹사이트에서 HTML 콘텐츠를 가져옴
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # '가장 많이 본 기사' 섹션을 찾음
    top_articles = soup.find_all('div', class_='auto-article', limit=1)

    # 각 기사의 제목, 링크, 그리고 내용을 추출
    for article in top_articles:
        title = article.find('a').get_text().strip()
        link = article.find('a')['href']
        full_link = url + link
        content = get_article_content(full_link)
        blog_contents = reformat_content_for_blog(text=content,title=title)
        print("blog_contents:", blog_contents)
        retitle, re_blog_contents = extract_title_and_content(blog_contents)
        re_blog_contents = get_html_tag(re_blog_contents)
        re_blog_contents += "\n<p>출처 AITimes: "+full_link+"<p>"
        tistory.postWrite(blog_name="wzacorn", title=retitle, content=re_blog_contents)
    
    return "완료"



print("파이썬 시작")
# 함수 실행
AI_url = 'https://www.aitimes.com/'
print(get_top_articles(AI_url))

# 카테고리 id를 받아오는 함수. default는 news 카
# tistory.CategoryList(blog_name="wzacorn")

