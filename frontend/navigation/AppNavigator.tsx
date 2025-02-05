import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import HomeScreen from '../screens/HomeSreen';
import AddPerformerScreen from '../screens/AddPerformerScreen';

const Stack = createNativeStackNavigator();
//   <Text style={styles.header}>List of Performers</Text>
export default function AppNavigator() {
  return (
    <Stack.Navigator initialRouteName="Home">
      <Stack.Screen name="List of Performers" component={HomeScreen} />
      <Stack.Screen name="Add Performer" component={AddPerformerScreen} />
    </Stack.Navigator>
  );
}
