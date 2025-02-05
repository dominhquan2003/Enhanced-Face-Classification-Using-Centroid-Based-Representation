import React from 'react';
import { Stack } from 'expo-router';
import color from '../contains/color';

const Layout = () => {
  return (
    <Stack>
      <Stack.Screen
        name="index" // Đường dẫn cho HomeScreen
        options={{
          title: 'List of Performers',
          headerTintColor: color.primary,
          headerTitleStyle: {
            fontWeight: 'bold',
          },
        }}
      />
      <Stack.Screen
        name="add-performer"
        options={{
          title: 'Add Performer',
        }}
      />
    </Stack>
  );
};

export default Layout;