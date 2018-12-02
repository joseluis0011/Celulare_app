import React from 'react';


const ProductsList = (props) => {
  return (
    <div>
      <table className="table is-narrow is-striped is-fullwidth is-hoverable">
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Cantidad</th>
          <th>Serie</th>
          <th>Modelo</th>
          <th>Marca</th>
        </tr>
      </thead>
      <tbody>
      {
        props.products.map((product) => {
          return (
            <tr key={product.id}>
            <td>{ product.nombre}</td>
            <td>{ product.cantidad}</td>
            <td>{ product.serie}</td>
            <td>{ product.modelo}</td>
            <td>{ product.marca}</td>
            </tr>
          )
        })
      }
      </tbody>
      </table>
    </div>
  )
};


export default ProductsList;