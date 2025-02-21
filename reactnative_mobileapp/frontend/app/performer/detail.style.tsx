import { Dimensions, StyleSheet } from 'react-native';
import color from '../../contains/color';

const { width } = Dimensions.get('window'); // Lấy chiều rộng của màn hình
const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    padding: 10,
  },

  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: '100%',
    marginTop: 12,
  },
  imageContainer: {
    alignItems: 'center',
    marginBottom: 15,
    flex: 1,
    paddingHorizontal: 5,
  },
  imageLarge: {
    width: width * 0.4,
    height: width * 0.45,
    borderRadius: 10,
  },

  imageSmall: {
    width: width * 0.25,
    height: width * 0.3,
    borderRadius: 10,
  },
  label: {
    fontSize: 14,
    fontWeight: 'bold',
    marginTop: 5,
    color: color.primary,
  },
  modalContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.7)'
  },
  closeIcon: {
    color: 'white',
    fontSize: 26,
   
  },
  modalImage: { width: '90%', height: '80%', resizeMode: 'contain' },
  closeIconCover: { position: 'absolute', top: 40, right: 20 },


});

export default styles;