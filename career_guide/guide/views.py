import openai
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# Set the OpenAI API key from settings
openai.api_key = settings.OPENAI_API_KEY

def home(request):
    return render(request, 'home.html')

@csrf_exempt
def get_roadmap(request):

    # List available models
    #models = openai.Model.list()
    #for model in models['data']:
        #print(model['id'])

    if request.method == 'POST':
        # Retrieve the career path from the POST request
        career = request.POST.get('career')
        
        # Check if career is provided
        if not career:
            return JsonResponse({"error": "Career is required"}, status=400)

        try:
            # Form the prompt for OpenAI API
            prompt = f"Create a detailed roadmap for becoming a {career}. Include steps, free resources, and advice."
            
            # Make the API call to OpenAI using the updated method
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # You can also use "gpt-4" if available
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )

            # Check if response contains choices and the message content
            if 'choices' in response and len(response['choices']) > 0:
                roadmap = response['choices'][0]['message']['content'].strip()
                return JsonResponse({"roadmap": roadmap})
            else:
                return JsonResponse({"error": "No roadmap generated. Try again."}, status=500)

        except openai.error.OpenAIError as e:
            return JsonResponse({"error": f"OpenAI API error: {str(e)}"}, status=500)
        except Exception as e:
            return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
