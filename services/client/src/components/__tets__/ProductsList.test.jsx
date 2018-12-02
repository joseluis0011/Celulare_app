import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';
 
import ProductsList from '../ProductsList';
 
const products = [
  { 
    'marca': 'xiomi',
    'modelo': 'S4',
    'serie': 'MK3526',
    'cantidad': 12,
    'id': 1,
    'nombre': 'Sansung'
  },
  { 
    'marca': 'apple',
    'modelo': 'M5',
    'serie': 'JJ3526',
    'cantidad': 12,
    'id': 2,
    'nombre': 'ipone'
  }
];
 
test('ProductsList renders properly', () => {
  const wrapper = shallow(<ProductsList products={products}/>);
  const element = wrapper.find('h4');
  expect(element.length).toBe(2);
  expect(element.get(0).props.children).toBe('Oreo');
});

test('ProductsList renders a snapshot properly', () => {
  const tree = renderer.create(<ProductsList products={products}/>).toJSON();
  expect(tree).toMatchSnapshot();
});
