import streamlit as st
import requests


url = f'http://10.6.46.204:5001/ask'

def main():
    st.set_page_config(page_title="Chat Goiás Social", page_icon="chat.png")
    st.title('**Chat Goiás Social**')

    # iniciando o histórico do chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Exibir mensagens de bate-papo do histórico na nova execução do aplicativo
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            with st.chat_message(message["role"], avatar='chat.png'):
                st.markdown(message["content"])
        elif message["role"] == "user":
            with st.chat_message(message["role"], avatar="usuario.png"):
                st.markdown(message["content"])

    # Entrada do usuário
    if prompt := st.chat_input(placeholder = 'Faça uma pergunta para mim!', max_chars = 800):
        with st.chat_message("user", avatar="usuario.png"):
            st.markdown(prompt)
        # Adicionando a mensagem a lista de historico
        st.session_state.messages.append({"role": "user", "content": prompt})

        if(len(st.session_state.messages) < 20):
            chat_history = st.session_state.messages
        else:
            chat_history = st.session_state.messages

        try:
            response = requests.post(url, json={'input': prompt, 'chat_history': chat_history})
            response_data = response.json()
            # Exibir resposta do assistente no campo de mensagens de bate-papo
            with st.chat_message("assistant", avatar='chat.png'):
                st.markdown(response_data['answer'])
            # Adicionando a mensagem a lista de historico
            st.session_state.messages.append({"role": "assistant", "content": response_data['answer']})
        except:
            mensagem_erro = "Não conseguimos estabelecer uma conexão com a base de dados no momento. Estamos trabalhando para resolver esse problema o mais rápido possível. Por favor, tente novamente mais tarde."
            with st.chat_message("assistant", avatar='chat.png'):
                st.markdown(mensagem_erro)
            st.session_state.messages.append({"role": "assistant", "content": mensagem_erro})


if __name__ == '__main__':
    main()


