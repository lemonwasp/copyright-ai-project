import streamlit as st
from analysis import analyze_similarity
from blockchain import Blockchain
import json
import pandas as pd

st.title("AI 콘텐츠 저작권 분석")

user_input = st.text_area("AI가 생성한 콘텐츠 문단을 입력하세요 (3~5문장 추천):")

if 'chain' not in st.session_state:
    st.session_state.chain = Blockchain()

if st.button("유사도 분석 및 블록체인 기록"):
    if user_input:
        sim_result = analyze_similarity(user_input)
        st.write("📊 유사도 분석 결과:")
        st.json(sim_result)

        # ✅ 바로 sim_result를 사용하면 됨!
        df = pd.DataFrame.from_dict(sim_result, orient='index', columns=['유사도'])
        st.bar_chart(df)

        # ✅ top_match도 sim_result 기준으로
        top_match = max(sim_result, key=sim_result.get)
        st.markdown(f"🎯 가장 유사한 스타일: **{top_match}**")

        # 블록에 저장할 데이터 구성
        block_data = {
            "text": user_input,
            "similarity": sim_result
        }
        st.session_state.chain.add_block(json.dumps(block_data))  # ✅ 문자열로 저장

        st.success("블록체인에 기록 완료!")
        st.write("🔐 마지막 블록 해시:", st.session_state.chain.get_latest_block().hash)
    else:
        st.warning("문단을 입력하세요.")


if st.button("📦 블록체인 전체 보기"):
    for block in st.session_state.chain.chain:
        st.text(f"Index: {block.index}, Hash: {block.hash}")
        try:
            parsed_data = json.loads(block.data)
            st.json(parsed_data)
            # 유사도 차트 시각화
            df = pd.DataFrame.from_dict(parsed_data['similarity'], orient='index', columns=['유사도'])
            st.bar_chart(df)
            # 가장 유사한 작가 표시
            top_match = max(parsed_data['similarity'], key=parsed_data['similarity'].get)
            st.markdown(f"🎯 가장 유사한 스타일: **{top_match}**")
        except Exception:
            st.write("🧱 데이터:", block.data)
            
