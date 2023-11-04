from rest_framework import  status
from rest_framework.response import Response
from social.models import FacebookPost, LinkedInPost, TwitterPost
from social.serializers import FacebookPostSerializer, LinkedInPostSerializer, TwitterPostSerializer
import requests
import json
from rest_framework.views import APIView

class CreateAndPublishPostView(APIView):

    def post(self, request, *args, **kwargs):
        platform = self.kwargs.get('platform')
        if platform == 'facebook':
            serializer = FacebookPostSerializer(data=request.data)
        elif platform == 'twitter':
            serializer = TwitterPostSerializer(data=request.data)
        elif platform == 'linkedin':
            serializer = LinkedInPostSerializer(data=request.data)
        else:
            return Response({'error': 'Invalid platform'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            
            serializer.save()
            access_token = ''
           
            message = serializer.data.get('message', '')

            if platform == 'facebook':
                page_id = ''
               
                post_url = f'https://graph.facebook.com/{page_id}/feed'
                
                payload = {
                    'message': message,
                    'access_token': access_token
                }
               
                response = requests.post(post_url, data=payload)
                
                if response.status_code == 200:
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'Failed to create post on Facebook'}, status=response.status_code)

            elif platform == 'twitter':
                tweet_text = message
                headers = {
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                }
                payload = {
                    "status": tweet_text
                }
                response = requests.post('https://api.twitter.com/1.1/statuses/update.json', headers=headers, json=payload)
                if response.status_code == 201:
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'Failed to create post on Twitter'}, status=response.status_code)

            elif platform == 'linkedin':
                linkedin_text = message
                linkedin_id = 'your_linkedin_id'
                headers = {
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                }
                payload = {
                    "author": f"urn:li:person:{linkedin_id}",
                    "lifecycleState": "PUBLISHED",
                    "specificContent": {
                        "com.linkedin.ugc.ShareContent": {
                            "shareCommentary": {
                                "text": linkedin_text
                            },
                            "shareMediaCategory": "NONE"
                        }
                    },
                    "visibility": {
                        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                    }
                }
                response = requests.post('https://api.linkedin.com/v2/ugcPosts', headers=headers, json=payload)
                if response.status_code == 201:
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'Failed to create post on LinkedIn'}, status=response.status_code)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeletePostView(APIView):
    def destroy(self, request, *args, **kwargs):
        platform = self.kwargs.get('platform')
        post_id = self.kwargs.get('post_id')
        access_token = 'your_access_token'

        if platform == 'facebook':
            delete_url = f'https://graph.facebook.com/{post_id}'
            payload = {
                'access_token': access_token
            }
            response = requests.delete(delete_url, data=payload)
            if response.status_code == 200:
                return Response({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'Failed to delete post on Facebook'}, status=response.status_code)

        elif platform == 'twitter':
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            response = requests.delete(f'https://api.twitter.com/1.1/statuses/destroy/{post_id}.json', headers=headers)
            if response.status_code == 200:
                return Response({'message': 'Tweet deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'Failed to delete tweet'}, status=response.status_code)

        elif platform == 'linkedin':
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            response = requests.delete(f'https://api.linkedin.com/v2/ugcPosts/{post_id}', headers=headers)
            if response.status_code == 200:
                return Response({'message': 'LinkedIn post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'Failed to delete LinkedIn post'}, status=response.status_code)

        else:
            return Response({'error': 'Invalid platform'}, status=status.HTTP_400_BAD_REQUEST)


class EditPostView(APIView):
    def put(self, request, *args, **kwargs):
        platform = self.kwargs.get('platform')
        post_id = self.kwargs.get('post_id')
        access_token = 'your_access_token'

        if platform == 'facebook':
            serializer = FacebookPostSerializer(data=request.data)
            endpoint = f'https://graph.facebook.com/{post_id}'
            payload = {
                'access_token': access_token,
                'message': serializer.data.get('message', '')
            }

        elif platform == 'twitter':
            serializer = TwitterPostSerializer(data=request.data)
            endpoint = f'https://api.twitter.com/1.1/statuses/update/{post_id}.json'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            payload = {
                "status": serializer.data.get('message', '')
            }

        elif platform == 'linkedin':
            serializer = LinkedInPostSerializer(data=request.data)
            endpoint = f'https://api.linkedin.com/v2/ugcPosts/{post_id}'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            payload = {
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": serializer.data.get('message', '')
                        }
                    }
                }
            }

        else:
            return Response({'error': 'Invalid platform'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            response = requests.put(endpoint, headers=headers, json=payload)
            if response.status_code == 200:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Failed to update post'}, status=response.status_code)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class FetchAllPostsView(APIView):
    def get(self, request, *args, **kwargs):
        platform = self.kwargs.get('platform')
        access_token = 'your_access_token'

        if platform == 'facebook':
            page_id = 'your_facebook_page_id'
            endpoint = f'https://graph.facebook.com/{page_id}/feed'
            params = {
                'access_token': access_token
            }
            response = requests.get(endpoint, params=params)
            if response.status_code == 200:
                posts_data = response.json().get('data', [])
                serializer = FacebookPostSerializer(data=posts_data, many=True)
                serializer.is_valid()
                return Response(posts_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Failed to fetch posts from Facebook'}, status=response.status_code)

        elif platform == 'twitter':
            headers = {
                'Authorization': f'Bearer {access_token}'
            }
            response = requests.get('https://api.twitter.com/2/tweets', headers=headers)
            if response.status_code == 200:
                posts_data = response.json().get('data', [])
                serializer = TwitterPostSerializer(data=posts_data, many=True)
                serializer.is_valid()
                return Response(posts_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Failed to fetch tweets'}, status=response.status_code)

        elif platform == 'linkedin':
            headers = {
                'Authorization': f'Bearer {access_token}'
            }
            response = requests.get('https://api.linkedin.com/v2/ugcPosts', headers=headers)
            if response.status_code == 200:
                posts_data = response.json().get('data', [])
                serializer = LinkedInPostSerializer(data=posts_data, many=True)
                serializer.is_valid()
                return Response(posts_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Failed to fetch LinkedIn posts'}, status=response.status_code)

        else:
            return Response({'error': 'Invalid platform'}, status=status.HTTP_400_BAD_REQUEST)