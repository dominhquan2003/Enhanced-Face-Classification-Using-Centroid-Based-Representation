import { StyleSheet } from 'react-native';
import color from '../../contains/color';
const styles = StyleSheet.create({
      item: {
            flexDirection: 'row',
            backgroundColor: color.white,
            marginBottom: 15,
            paddingVertical: 14,
            paddingHorizontal: 20,
            alignItems: 'center',
            justifyContent: 'space-between',
            borderRadius: 10,
      },
      square: {
            width: 48,
            height: 36,
            borderRadius: 12,
            backgroundColor: color.second,
            alignItems: 'center',
            justifyContent: 'center',
      },
      number: {
            color: color.white,
            fontWeight: '700',
      },
      content: {
            width: '80%',
            fontSize: 16,
            color: color.text
      },



});
export default styles;
