import streamlit as st
from google import genai
from streamlit_mic_recorder import mic_recorder

st.set_page_config(page_title="Lumi AI", page_icon="💡")
st.title("💡 Lumi - Sənin Şəxsi Süni İntellektin")
st.write("Salam! Mən dünyanın bütün dillərini mükəmməl bilən və səninlə səsli də danışa bilən ağıllı köməkçiyəm.")

# API açarını Streamlit Secrets-dən təhlükəsiz oxuyuruq
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ API açarı tapılmadı. Zəhmət olmasa Streamlit Secrets bölməsinə GEMINI_API_KEY əlavə edin!")
else:
    client = genai.Client(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Səs yazma düyməsi
    st.write("🎙️ **Səslə danışmaq üçün aşağıdakı düyməyə basıb danışın:**")
    audio_data = mic_recorder(start_prompt="🎙️ Danışmağa Başla", stop_prompt="⏹️ Dayandır və Göndər", key='mic')

    if audio_data:
        audio_bytes = audio_data['bytes']
        user_prompt = "Zəhmət olmasa bu səsli mesajı dinlə və Azərbaycan dilində cavab ver."
        
        st.session_state.messages.append({"role": "user", "content": "🎙️ [Səsli mesaj göndərildi]"})
        with st.chat_message("user"):
            st.markdown("🎙️ [Səsli mesaj göndərildi]")

        with st.chat_message("assistant"):
            with st.spinner("Lumi səni dinləyir və düşünür..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[
                            user_prompt,
                            {"mime_type": "audio/wav", "data": audio_bytes}
                        ],
                        config={
                            'system_instruction': 'Sənin adın Lumi-dir. Sən dünyanın bütün dillərini mükəmməl bilən, son dərəcə intellektual, nəzakətli, dəqiq və səsli mesajları başa düşüb cavab verən super süni intellekt köməkçisisən.'
                        }
                    )
                    answer = response.text
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Xəta baş verdi: {e}")

    # Mətn ilə də yaza bilmək üçün
    if user_input := st.chat_input("Və ya sualınızı yazı ilə yazın..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Lumi düşünür..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=user_input,
                        config={
                            'system_instruction': 'Sənin adın Lumi-dir. Sən dünyanın bütün dillərini mükəmməl bilən, son dərəcə intellektual, nəzakətli, dəqiq və istifadəçiyə hərtərəfli kömək edən super süni intellekt köməkçisisən.'
                        }
                    )
                    answer = response.text
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Xəta baş verdi: {e}")

