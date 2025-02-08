import { Alert } from "react-native";

export const handlePost = async (performerName : string, onPostSuccess: any) => {
      const requestOptions = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          "Access-Control-Allow-Origin": "*",
        },
        body: JSON.stringify({
          name: performerName,
          status: true,
          original_image: null,
          detected_image: null,
          heatmap_1: null,
          heatmap_2: null,
          heatmap_3: null,
        }),
      };
    
      try {
        const apiUrl = process.env.EXPO_PUBLIC_API_URL;
        const response = await fetch(apiUrl, requestOptions);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Success:', data);
        Alert.alert('Success', 'Performance added successfully!');
        
        // Gọi callback để thông báo về việc post thành công
        onPostSuccess();
      } catch (error) {
        console.error('Error:', error);
      }
    };