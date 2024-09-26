from django.shortcuts import render
from dotenv import load_dotenv
load_dotenv()
import os
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .serializers import FileUploadSerializer
import groq

import logging
logger = logging.getLogger(__name__)

class SentimentAnalysisView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    serializer_class = FileUploadSerializer
    template_name = 'groq_api/upload.html'

    def get(self, request):
        serializer = self.serializer_class()
        return Response({'serializer': serializer}, template_name=self.template_name)

    def post(self, request, format=None):
        logger.info("Post method called")
        logger.info(f"Request data: {request.data}")
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            logger.info("Serializer is valid")
            file = serializer.validated_data['file']
            
            try:
                # Read the file
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                elif file.name.endswith('.xlsx'):
                    df = pd.read_excel(file)
                else:
                    error_message = 'Invalid file format. Please upload a CSV or XLSX file.'
                    logger.error(error_message)
                    if request.accepted_renderer.format == 'html':
                        return Response({'error': error_message}, template_name=self.template_name, status=status.HTTP_400_BAD_REQUEST)
                    return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
                
                # Extract reviews
                reviews = df['Review'].tolist()[:50]  # Limit tReviews
                logger.info(f"Extracted {len(reviews)} reviews")
                
                # Perform sentiment analysis using Groq API
                client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
                
                positive_count = 0
                negative_count = 0
                neutral_count = 0
                
                for review in reviews:
                    prompt = f"Analyze the sentiment of the following review. Respond with only one word: POSITIVE, NEGATIVE, or NEUTRAL.\n\nReview: {review}"
                    
                    response = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "You are a sentiment analysis expert. Analyze the given text and respond with one word: POSITIVE, NEGATIVE, or NEUTRAL."},
                            {"role": "user", "content": prompt}
                        ],
                        model="mixtral-8x7b-32768",
                        temperature=0
                    )
                    
                    sentiment = response.choices[0].message.content.strip().upper()
                    
                    if sentiment == "POSITIVE":
                        positive_count += 1
                    elif sentiment == "NEGATIVE":
                        negative_count += 1
                    else:
                        neutral_count += 1
                
                total_reviews = len(reviews)
                result = {
                    "positive": positive_count / total_reviews,
                    "negative": negative_count / total_reviews,
                    "neutral": neutral_count / total_reviews
                }
                
                logger.info(f"Analysis complete. Result: {result}")
                
                if request.accepted_renderer.format == 'html':
                    logger.info("Returning HTML response")
                    return Response({'result': result}, template_name='groq_api/results.html')
                logger.info("Returning JSON response")
                return Response(result, status=status.HTTP_200_OK)
            
            except Exception as e:
                error_message = str(e)
                logger.error(f"An error occurred: {error_message}")
                if request.accepted_renderer.format == 'html':
                    return Response({'error': error_message}, template_name=self.template_name, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        logger.error(f"Serializer errors: {serializer.errors}")
        if request.accepted_renderer.format == 'html':
            return Response({'serializer': serializer}, template_name=self.template_name)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

