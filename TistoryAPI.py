import requests
import os, json

# client_id == client_id
client_id = "68b7368ceec4522809c75ab1a00553ea"
secret_key = "68b7368ceec4522809c75ab1a00553ea2c78d36135d7f26e02e6d843a5cf43e5755e276f"
access_token = "5d692352dbcea2d43384a81c7f459de1_0590de3c23fcadafa068dfcb97ff68b4"
redirect_uri = "https://wzacorn.tistory.com/"

# 인증 요청 및 Authentication code 발급
# https://tistory.github.io/document-tistory-apis/auth/authorization_code.html
def getAuthenticationCode():
    response_type = "code"
    state = "anything"
    url = "https://www.tistory.com/oauth/authorize?" + \
          "client_id=" + client_id + "&" + \
          "redirect_uri=" + redirect_uri + "&" + \
          "response_type=" + response_type
    return url

# Access Token 발급
# https://tistory.github.io/document-tistory-apis/auth/authorization_code.html
def getAccessToken():
    code = "89662e9ccc695e1ebb24ff698c82515a19507b243d8ca15bccd829166f82f57d7ab31c6a"
    grant_type = "authorization_code"

    url = "https://www.tistory.com/oauth/access_token?" + \
          "client_id=" + client_id + "&" + \
          "client_secret=" + secret_key + "&" + \
          "redirect_uri=" + redirect_uri + "&" + \
          "code=" + code + "&" + \
          "grant_type=" + grant_type

    try:
        res = requests.get(url)
        return res
    except json.JSONDecodeError:
        print("JSON decoding error. Response was:", res)
        return None


# 자신의 블로그 정보
# https://tistory.github.io/document-tistory-apis/apis/v1/blog/list.html
def BlogInfo(output_type="json"):
    url = "https://www.tistory.com/apis/blog/info?" + \
          "access_token=" + access_token + "&" + \
          "output=" + output_type
    res = requests.get(url).text  # 변경된 부분: .content 대신 .text 사용
    print("getBLogInfo : ", url)
    try:
        return json.loads(res)
    except json.JSONDecodeError:
        print("JSON decoding error. Response was:", res)
        return None


# 글 목록
# https://tistory.github.io/document-tistory-apis/apis/v1/post/list.html
def PostList(blog_name, page=1, output='xml'):
    url = "https://www.tistory.com/apis/post/list?"
    url += "access_token=" + access_token + "&"
    url += "output=" + output + "&"
    url += "blogName=" + blog_name + "&"
    url += "page=" + str(page) + "&"
    res = requests.get(url).content
    print("getPostList : ", url)
    return json.loads(res)

# 글 읽기
# https://tistory.github.io/document-tistory-apis/apis/v1/post/read.html
def PostRead(blog_name,post_id):
    url = "https://www.tistory.com/apis/post/read?"
    url += "access_token=" + access_token + "&"
    #url += "output=" + output + "&"
    url += "blogName=" + blog_name + "&"
    url += "postId=" + str(post_id) + "&"
    res = requests.get(url).content

    print("getPostRead : ", url)
    return json.loads(res)

# 글 작성
# https://tistory.github.io/document-tistory-apis/apis/v1/post/write.html
def postWrite(blog_name, title, content="", output_type="json"):
    url = "https://www.tistory.com/apis/post/write?"
    url += "access_token=" + access_token + "&"
    url += "output=" + output_type + "&"
    url += "blogName=" + blog_name + "&"
    url += "title=" + title + "&"
    url += "content=" + content + "&"

    #data += "category=" + "1024642"
    try:
        res = requests.post(url).text
        return json.loads(res)
    except json.JSONDecodeError:
        print("JSON decoding error. Response was:", res)
        return None
    

# 글 수정
# https://tistory.github.io/document-tistory-apis/apis/v1/post/modify.html
def postModify(blog_name, title, content="", visibility=0, category_id=0, published=None, slogan=None, tag=None,
              acceptComment=1, password=None, output_type="xml"):
    url = "https://www.tistory.com/apis/post/modify?"
    url += "access_token=" + access_token + "&"
    url += "output=" + output_type + "&"
    url += "blogName=" + blog_name + "&"
    url += "title=" + title + "&"
    url += "content=" + content + "&"
    url += "visiblility=" + visibility + "&"
    url += "category=" + category_id + "&"
    url += "published=" + published + "&"
    url += "slogan=" + slogan + "&"
    url += "tag=" + tag + "&"
    url += "acceptComment=" + acceptComment + "&"
    url += "password=" + password + "&"

# 파일 첨부
# https://tistory.github.io/document-tistory-apis/apis/v1/post/attach.html
#tageturl은 api 문서에 없는데 이걸 넣어야지 썸네일 자동등록됨
def postAttach(blog_name, file_name=None):
    url = "https://www.tistory.com/apis/post/attach?"
    url += "access_token=" + access_token + "&"
    url += "blogName=" + blog_name + "&"
    url += 'targetUrl' + blog_name + "&"
    url += "output=json"
    file = dict(uploadedfile=open(file_name, 'rb'))
    res = requests.post(url, files=file).content
    print("postAttach : ", url)

    return json.loads(res)

# 카테고리
# https://tistory.github.io/document-tistory-apis/apis/v1/category/list.html
def CategoryList(blog_name, output='xml'):
    url = "https://www.tistory.com/apis/category/list?"
    url += "access_token=" + access_token + "&"
    url += "output=" + output + "&"
    url += "blogName=" + blog_name

    print("getCategoryID : ", url)
    res = requests.get(url).content
    return json.loads(res)

# 최근 댓글 목록
# https://tistory.github.io/document-tistory-apis/apis/v1/comment/recent.html
def CommentNewest(blog_name, page=1, count=10, output_type="xml"):
    url = "https://www.tistory.com/apis/comment/newest?"
    url += "access_token=" + access_token + "&"
    url += "output=" + output_type + "&"
    url += "blogName=" + blog_name + "&"
    url += "page=" + page + "&"
    url += "count=" + count

    print("getCommentNewest : ", url)
    res = requests.get(url).content
    return json.loads(res)

# 댓글 목록
# https://tistory.github.io/document-tistory-apis/apis/v1/comment/list.html
def CommentList(blog_name, post_id, output_type="xml"):
    url = "https://www.tistory.com/apis/comment/list?"
    url += "access_token=" + access_token + "&"
    url += "output=" + output_type + "&"
    url += "blogName=" + blog_name + "&"
    url += "page=" + post_id

    print("getCommentList : ", url)
    res = requests.post(url).content
    return json.loads(res)

# 댓글 작성
# https://tistory.github.io/document-tistory-apis/apis/v1/comment/write.html
def CommentWrite(blog_name, post_id, parent_id, content, secret=0, output_type="xml"):
    url = "https://www.tistory.com/apis/comment/write?"
    url += "access_token=" + access_token + "&"
    url += "output=" + output_type + "&"
    url += "blogName=" + blog_name + "&"
    url += "page=" + post_id + "&"
    url += "parentId="+parent_id + "&"
    url += "content="+content + "&"
    url += "secret="+secret

    print("CommentWrite : ", url)
    res = requests.post(url).content
    return json.loads(res)

# 댓글 수정
# https://tistory.github.io/document-tistory-apis/apis/v1/comment/modify.html
def CommentModify(blog_name, post_id, comment_id, content, secret=0, output_type="xml"):
    url = "https://www.tistory.com/apis/comment/modify?"
    url += "access_token=" + access_token + "&"
    url += "output=" + output_type + "&"
    url += "blogName=" + blog_name + "&"
    url += "page=" + post_id + "&"
    url += "commentId=" + comment_id + "&"
    url += "content=" + content + "&"
    url += "secret=" + secret

    print("CommentNodify : ", url)
    res = requests.post(url).content
    return json.loads(res)

# 댓글 삭제
# https://tistory.github.io/document-tistory-apis/apis/v1/comment/delete.html
def CommentDelete(blog_name, post_id, comment_id, output_type="xml"):
    url = "https://www.tistory.com/apis/comment/modify?"
    url += "access_token=" + access_token + "&"
    url += "output=" + output_type + "&"
    url += "blogName=" + blog_name + "&"
    url += "page=" + post_id + "&"
    url += "commentId=" + comment_id + "&"

    print("CommentDelete : ", url)
    res = requests.post(url).content
    return json.loads(res)


if __name__ == "__main__":
    postWrite("wzacorn",)


