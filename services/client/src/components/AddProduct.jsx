import React from 'react';
const AddProduct= (props) => {
    return (
    <form onSubmit={(event) => props.addProduct(event)}>
        <div className="field">
        <div className="control">
        <input
        name="nombre"
        className="input is-large"
        type="text"
        placeholder="celular"
        required
        value={props.nombre}
        onChange={props.handleChange}
        />
        </div>
        </div>
        <div className="field">
        <input
        name="cantidad"
        className="input is-large"
        type="text"
        placeholder="cantidad"
        required
        value={props.cantidad}
        onChange={props.handleChange}
        />
        </div>
        <div className="field">
        <input
        name="serie"
        className="input is-large"
        type="text"
        placeholder="serie"
        required
        value={props.serie}
        onChange={props.handleChange}
        />
        </div>
        <div className="field">
        <input
        name="modelo"
        className="input is-large"
        type="text"
        placeholder="modelo"
        required
        value={props.modelo}
        onChange={props.handleChange}
        />
        </div>
        <div className="field">
        <input
        name="marca"

        className="input is-large"
        type="text"
        placeholder="marca"
        required
        value={props.marca}
        onChange={props.handleChange}
        />
        </div>
        <div className="field">
        <input
        type="submit"
        className="button is-primary is-large is-rounded is-fullwidth"
        value="Registrar"
        />
        </div>
        </form>
        )
    };

export default AddProduct;