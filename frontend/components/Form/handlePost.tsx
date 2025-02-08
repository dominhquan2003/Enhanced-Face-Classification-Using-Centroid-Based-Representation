import { router } from "expo-router";
import { Alert } from "react-native";
import { useTaskContext } from '../../context/TaskContext';
export const handlePost = async (
  performerName: string,
  selectedImage: string | null,
  onPostSuccess: any,
  addTask: (newTask: { id: number; name: string }) => void
) => {
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
    const response = await fetch(apiUrl, requestOptions);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    useTaskContext
    console.log('Success:', data);
    Alert.alert('Success', 'Performance added successfully!');
    addTask({ id: data.id, name: performerName });
    onPostSuccess();
    router.push(`/performer/${data.id}`);
  } catch (error) {
    console.error('Error:', error);
    Alert.alert('Error', 'Failed to add performer.');
  }
};
