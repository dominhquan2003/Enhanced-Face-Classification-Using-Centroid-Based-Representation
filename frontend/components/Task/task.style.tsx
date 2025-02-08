import { StyleSheet } from 'react-native';
import color from '../../contains/color';
const styles = StyleSheet.create({
      shadowContainer: {
            backgroundColor: 'transparent', 
            borderRadius: 10, 
            marginBottom: 20, 
            shadowColor: '#000', 
            shadowOffset: { width: 0, height: 0 }, 
            shadowOpacity: 0.3, 
            shadowRadius: 6, 
            elevation: 8, 
            marginHorizontal: 10, 
      },
      item: {
            flexDirection: 'row',
            backgroundColor: 'white',
            paddingVertical: 14,
            paddingHorizontal: 20,
            alignItems: 'center',
            justifyContent: 'space-between',
            borderRadius: 10, 
            overflow: 'hidden', 
      },
      square: {
            width: 48,
            height: 36,
            borderRadius: 12,
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: color.badge2,
      },
      number: {
            color: color.white,
            fontWeight: '700',
      },
      content: {
            width: '80%',
            fontSize: 17,
            color: color.text,
      },
      squareOdd: {
            backgroundColor: color.badge1,
      },
      squareEven: {
            backgroundColor: color.badge2,
      },
});
export default styles;
