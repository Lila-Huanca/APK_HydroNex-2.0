# Hydro-Bot
if choice == "Hydro-Bot":
    st.title("Hydro-Bot")
    st.write("¡Hola! Bienvenido al chatbot 'Hydro-Bot'. Puedes consultar el estado de tu dispositivo HydroNex aquí.")
    st.subheader("Temas sugeridos para preguntar:")
    st.markdown("""
    - **Estado del dispositivo**: "¿Cuál es el estado de llenado actual?"
    - **Historial de llenado**: "¿Cuál es el historial de llenado del dispositivo?"
    - **Litros acumulados**: "¿Cuántos litros hay acumulados?"
    """)

    user_query = st.text_input("¿Qué te gustaría saber acerca de tu HydroNex?")
    if user_query:
        if "llenado" in user_query.lower():
            # Verificar si el dispositivo está conectado o no
            if st.session_state["estado de hydronex"] == "en proceso de llenado":
                st.write(f"Asistente: El dispositivo actualmente está en {st.session_state['estado de hydronex']}.")
                # Simular cambio en el estado de llenado
                estados_llenado = ["en proceso de llenado", "a la mitad de la capacidad", "completamente lleno"]
                estado_actual = estados_llenado.index(st.session_state["estado de hydronex"])
                st.session_state["estado de hydronex"] = estados_llenado[(estado_actual + 1) % len(estados_llenado)]
            else:
                st.write("Asistente: El dispositivo no está conectado, escribe a soporte.")
        elif "condición" in user_query.lower():
            condicion = "óptimas" if st.session_state["condición de hydronex"] == "apto" else "malas"
            st.write(f"Asistente: El dispositivo está en condiciones {condicion}.")
        elif "historial" in user_query.lower():
            st.write("Asistente: El historial de llenado es el siguiente:")
            st.write(st.session_state["historial de Hydronex"])
        elif "litros acumulados" in user_query.lower():
            if st.session_state["litros acumulados"] == 0:
                st.write("Asistente: Actualmente no tenemos litros acumulados. Por favor, espera un momento y vuelve a preguntar.")
                st.session_state["litros acumulados"] = 150  # Simular acumulación
            else:
                st.write(f"Asistente: El dispositivo tiene {st.session_state['litros acumulados']} litros acumulados.")
        else:
            st.write("Asistente: Lo siento, no puedo responder esa pregunta. Intente preguntar sobre el estado, la condición o el historial del dispositivo.")
