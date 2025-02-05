// import { StatusBar } from 'expo-status-bar';
// import { Text, View } from 'react-native';
// import Task from './components/Task';
// import styles from './App.component.style';
// import Form from './components/Form/index';
// import React, { useState } from 'react';

// export default function App() {
//   const [refreshTrigger, setRefreshTrigger] = useState(0);

//   const handlePostSuccess = () => {
//     setRefreshTrigger(prev => prev + 1); 
//   };

//   return (
//     <View style={styles.container}>
//       <View style={styles.body}>
//         <Text style={styles.header}>List of Performers</Text>
        
//         <Task refreshTrigger={refreshTrigger} />
//       </View>
      
//       {/* Truyền handlePostSuccess xuống Form để cập nhật Task */}
//       <Form onPostSuccess={handlePostSuccess} />

//       <StatusBar style="auto" />
//     </View>
//   );
// }
import 'react-native-gesture-handler';
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import AppNavigator from './navigation/AppNavigator';

export default function App() {
  return (
    <NavigationContainer>
      <AppNavigator />
    </NavigationContainer>
  );
}
