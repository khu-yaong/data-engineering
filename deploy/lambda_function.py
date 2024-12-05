import json
import pandas as pd

# Lambda 핸들러
def handler(event, context):

    # 입력 데이터 처리
    body = event['body']
    video_ids = body['videoIds']

    # 예측 수행
    try:
        video_df = pd.read_pickle("video_df.pkl")
        cosine_sim = pd.read_pickle("cosine_sim.pkl")
    except Exception as e:
        raise ValueError(f"Error loading model: {e}")
    
    final_video_indices = []
    for video_id in video_ids:

        try:
            idx = video_df[video_df["videoId"] == video_id].index[0]
        except IndexError:
            print("null")
            return None

        # 해당 영상에 대한 유사도 측정
        sim_scores = list(enumerate(cosine_sim[idx]))

        # 유사도에 따라 정렬
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # 상위 10개 영상 선택
        sim_scores = sim_scores[1:11]

        # 선택된 영상의 인덱스
        final_video_indices += [i[0] for i in sim_scores]

    # 선택된 영상의 제목으로 반환
    final_video_indices = list(set(final_video_indices))[:10]
    final_titles = video_df['title'].iloc[final_video_indices].tolist()

    # 추천된 영상 제목을 JSON 형태로 반환
    prediction = json.dumps({'recommended_titles': final_titles})

    # 결과 반환
    return {
        'statusCode': 200,
        'body': prediction
    }

'''
if __name__ == "__main__":

    # 예시 입력 데이터
    event = {
        "body": json.dumps({
                "videoIds": ["AfPaDw2upuk", "Dru7TvHX7lY"]
            })
    }
    # Lambda 핸들러 호출
    response = handler(event, None)
    print(response)
'''

