import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [menuItems, setMenuItems] = useState([]);
  const [orderItems, setOrderItems] = useState({});
  const [filteredItems, setFilteredItems] = useState([]);
  const [openCategory, setOpenCategory] = useState(null);
  const [searchTerm, setSearchTerm] = useState(""); // Trạng thái cho tìm kiếm

  useEffect(() => {
    axios
      .get("https://restaurant-backend-v.up.railway.app/api/menu-items/")
      .then((res) => {
        setMenuItems(res.data);
        setFilteredItems(res.data); // Hiển thị tất cả sản phẩm ban đầu
      })
      .catch((err) => console.error("Lỗi khi lấy menu:", err));
  }, []);

  const handleFilter = (category) => {
    if (category === "") {
      setFilteredItems(menuItems); // Hiển thị tất cả nếu không chọn nhóm
    } else {
      setFilteredItems(menuItems.filter((item) => item.category === category));
    }
  };

  const toggleCategory = (category) => {
    setOpenCategory(openCategory === category ? null : category);
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
    setFilteredItems(
      menuItems.filter((item) =>
        item.name.toLowerCase().includes(e.target.value.toLowerCase())
      )
    );
  };

  const handleSort = (order) => {
    const sortedItems = [...filteredItems].sort((a, b) => {
      if (order === "asc") return a.price - b.price;
      if (order === "desc") return b.price - a.price;
      return 0;
    });
    setFilteredItems(sortedItems);
  };

  const handleAdd = (itemId) => {
    setOrderItems((prevOrderItems) => {
      const newOrderItems = { ...prevOrderItems };
      newOrderItems[itemId] = (newOrderItems[itemId] || 0) + 1;
      return newOrderItems;
    });
  };

  const handleSubmitOrder = () => {
    const items = Object.entries(orderItems).map(([item_id, quantity]) => ({
      item: parseInt(item_id),
      quantity,
    }));

    console.log("Dữ liệu gửi đi:", { items });

    axios
      .post("https://restaurant-backend-v.up.railway.app/api/orders/", {
        items,
      })
      .then((res) => {
        alert("✅ Đơn hàng đã được tạo!");
        setOrderItems({});
      })
      .catch((err) => console.error("❌ Lỗi khi tạo đơn hàng:", err));
  };

  const calculateTotal = () => {
    return Object.entries(orderItems).reduce((total, [id, qty]) => {
      const item = menuItems.find((i) => i.id === parseInt(id));
      return total + (item?.price || 0) * qty;
    }, 0);
  };

  const formatPrice = (price) => {
    return `${parseInt(price).toLocaleString()} VND`; // Loại bỏ phần thập phân và thêm dấu phân cách
  };

  return (
    <div className="app-container">
      <h1 className="menu-title">🍽️ Menu nhà hàng</h1>

      {/* Thanh tìm kiếm và lọc giá */}
      <div className="search-and-price-container">
        <div className="search-container">
          <input
            type="text"
            placeholder="Tìm kiếm món ăn..."
            value={searchTerm}
            onChange={handleSearch}
          />
        </div>
        <div className="price-filter-container">
          <select onChange={(e) => handleSort(e.target.value)} defaultValue="">
            <option value="" disabled>
              Lọc giá
            </option>
            <option value="asc">Giá: Thấp đến cao</option>
            <option value="desc">Giá: Cao đến thấp</option>
          </select>
        </div>
      </div>

      <div className="content-container">
        {/* Phần lọc sản phẩm */}
        <div className="filter-container">
          <button onClick={() => handleFilter("")}>Tất cả</button>
          <button onClick={() => handleFilter("mi")}>Mì</button>
          <button onClick={() => handleFilter("com")}>Cơm</button>
          <button onClick={() => toggleCategory("nuoc")}>Nước uống</button>
          {openCategory === "nuoc" && (
            <div className="sub-filter-container">
              <button onClick={() => handleFilter("nuoc_tra_sua")}>
                Trà sữa
              </button>
              <button onClick={() => handleFilter("nuoc_tra")}>Trà</button>
              <button onClick={() => handleFilter("nuoc_topping")}>
                Topping
              </button>
              <button onClick={() => handleFilter("nuoc_khac")}>
                Các loại khác
              </button>
            </div>
          )}
          <button onClick={() => handleFilter("anvat")}>Ăn vặt</button>
          <button onClick={() => handleFilter("mon_them")}>Món thêm</button>
        </div>

        {/* Phần sản phẩm */}
        <div className="menu-container">
          {filteredItems.map((item) => (
            <div className="menu-item" key={item.id}>
              <h3>{item.name}</h3>
              <p>Giá: {formatPrice(item.price)}</p>
              <button onClick={() => handleAdd(item.id)}>Thêm vào giỏ</button>
            </div>
          ))}
        </div>

        {/* Phần đơn đặt hàng */}
        <div className="order-container">
          <h2>📝 Đơn đặt hiện tại</h2>
          <ul className="order-list">
            {Object.entries(orderItems).map(([id, qty]) => {
              const item = menuItems.find((i) => i.id === parseInt(id));
              return (
                <li key={id}>
                  {item?.name} x {qty} = {formatPrice((item?.price || 0) * qty)}
                </li>
              );
            })}
          </ul>
          <h3>💰 Tổng tiền: {formatPrice(calculateTotal())}</h3>
          {Object.keys(orderItems).length > 0 && (
            <button className="confirm-button" onClick={handleSubmitOrder}>
              ✅ Xác nhận đơn
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
