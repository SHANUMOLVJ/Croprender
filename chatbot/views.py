from django.shortcuts import render

# Create your views here.
import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse

# Set your Gemini API key
API_KEY = 'AIzaSyCSrEWAwXi7JJ6AtOx5Xq6HKJukAyHYsn8'
genai.configure(api_key=API_KEY)

def chatbot_view(request):
    return render(request, 'chatbot/chatbot.html')

def get_response(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        conversation_history = request.session.get('conversation_history', [])

        # Add user input to the conversation history
        conversation_history.append(f"You: {user_input}")

        # Create a prompt for the chatbot
        prompt = f"""
        The following is a conversation with a helpful assistant. The assistant is helpful, creative, clever, and very friendly.
        {" ".join(conversation_history)}
        Assistant:
        """

        # Generate the chatbot's response
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        chatbot_reply = response.text.strip()

        # Add the chatbot's reply to the conversation history
        conversation_history.append(f"Assistant: {chatbot_reply}")
        request.session['conversation_history'] = conversation_history

        return JsonResponse({'reply': chatbot_reply})

    return JsonResponse({'error': 'Invalid request'}, status=400)
