import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios'; //nuevo
import ProductsList from './components/ProductsList';
import AddProduct from './components/AddProduct';

//nuevo
class App extends Component {

	constructor(){
		super();
		this.state ={
			products: [],
			nombre: '',
			cantidad: '',
			serie: '',
			modelo: '',
			marca: '',
		};
		this.addProduct = this.addProduct.bind(this);
		this.handleChange = this.handleChange.bind(this);
	};

    //nuevo
	componentDidMount() {
		this.getProducts();
	};

	// nuevo
	getProducts() {
		axios.get(`${process.env.REACT_APP_PRODUCTS_SERVICE_URL}/products`)
		.then((res) => { this.setState({ products: res.data.data.products }); }) 
		.catch((err) => { console.log(err); });
	}

	addProduct(event) {
		event.preventDefault();
		const data = {
			nombre: this.state.nombre,
			cantidad: this.state.cantidad,
			serie: this.state.serie,
			modelo: this.state.modelo,
			marca: this.state.marca
		};
		axios.post(`${process.env.REACT_APP_PRODUCTS_SERVICE_URL}/products`,data)
		.then((res) => { 
			this.getProducts();
			this.setState({ 
				nombre: '', 
				cantidad: '', 
				serie: '', 
				modelo: '', 
				marca: ''});
		 })
		.catch((err) => { console.log(err); });
	};

	handleChange(event){
		const obj = {};
		obj[event.target.name] = event.target.value;
		this.setState(obj);
	};

	render(){
		return (
			<section className="section">
			<div className="container">
			<div className="columns">
			<div className="column is-one-third box">
			<br/>
			<h2 className="title is-1">Registrar Nuevo Celular</h2>
			<hr/><br/>
			<AddProduct
			nombre={this.state.nombre} 
			cantidad={this.state.cantidad} 
			serie={this.state.serie} 
			modelo={this.state.modelo} 
			marca={this.state.marca} 
			addProduct={this.addProduct} 
			handleChange={this.handleChange}
			/>
			</div>
			<div className="column">
			<br/>
			<h3 className="title is-1"> listar Productos de Celulares</h3>
			<hr/><br/>
			<ProductsList products={this.state.products}/>
			</div>
			</div>
			</div>
			</section>
		)
	}
}


ReactDOM.render(
	<App />,
	document.getElementById('root')
);
