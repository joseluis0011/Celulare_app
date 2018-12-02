import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import AddProduct from '../AddProduct';

test('AddProduct renders properly', () => {
    const wrapper = shallow(<AddProduct/>);
    const element = wrapper.find('form');
    expect(element.find('input').length).toBe(6);
    expect(element.find('input').get(0).props.name).toBe('nombre');
    expect(element.find('input').get(1).props.name).toBe('cantidad');
    expect(element.find('input').get(2).props.name).toBe('serie');
    expect(element.find('input').get(3).props.name).toBe('modelo');
    expect(element.find('input').get(4).props.name).toBe('marca');
    expect(element.find('input').get(5).props.type).toBe('submit');
});

test('AddProduct renders a snapshot properly', () => {
    const tree = renderer.create(<AddProduct/>).toJSON();
    expect(tree).toMatchSnapshot();
});
