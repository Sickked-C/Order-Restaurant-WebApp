import React from "react";

function MenuItem({ item, onAdd }) {
  return (
    <div
      style={{
        border: "1px solid #ccc",
        padding: "10px",
        margin: "10px",
        textAlign: "center",
      }}
    >
      <img
        src={item.image} // Hiển thị ảnh từ API
        alt={item.name}
        style={{
          width: "150px",
          height: "150px",
          objectFit: "cover",
          marginBottom: "10px",
        }}
      />
      <h3>{item.name}</h3>
      <p>{item.description}</p>
      <p>Giá: ${item.price}</p>
      <button onClick={() => onAdd(item.id)}>Thêm vào giỏ hàng</button>
    </div>
  );
}

export default MenuItem;
