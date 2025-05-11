// filepath: c:\Users\ASUS\restaurant_order_project\restaurant-order-frontend\src\pages\HomePage.js
import React, { useEffect, useState } from "react";
import axios from "axios";
import MenuItem from "../components/MenuItem";

function HomePage() {
  const [menuItems, setMenuItems] = useState([]);

  useEffect(() => {
    axios
      .get("https://restaurant-backend-v.up.railway.app/api/menu-items/")
      .then((res) => setMenuItems(res.data))
      .catch((err) => console.error("Lỗi khi lấy menu:", err));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>🍽️ Menu nhà hàng</h1>
      <div style={{ display: "flex", flexWrap: "wrap" }}>
        {menuItems.map((item) => (
          <MenuItem key={item.id} item={item} />
        ))}
      </div>
    </div>
  );
}

export default HomePage;
