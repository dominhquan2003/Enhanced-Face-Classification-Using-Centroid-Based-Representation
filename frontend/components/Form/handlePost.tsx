import { router } from "expo-router";
import { Alert } from "react-native";

export const handlePost = async (performerName: string, selectedImage: string | null, onPostSuccess: any) => {
  try {
    const apiUrl = process.env.EXPO_PUBLIC_API_URL;
    const formData = new FormData();
    formData.append('name', performerName);
    formData.append('status', 'true');
    if (selectedImage) {
      const fileName = selectedImage.split('/').pop();
      const fileType = fileName?.split('.').pop();

      formData.append('original_image', {
        uri: selectedImage,
        name: fileName,
        type: `image/${fileType}`,
      } as any);
    }

    const requestOptions = {
      method: 'POST',
      headers: {
        'Content-Type': 'multipart/form-data',
        "Access-Control-Allow-Origin": "*",
      },
      body: formData,
    };
    Alert.alert('Success', 'Performance added successfully!');
    onPostSuccess();
    router.push('/');
  } catch (error) {
    console.error('Error:', error);
    Alert.alert('Error', 'Failed to add performer.');
  }
};
