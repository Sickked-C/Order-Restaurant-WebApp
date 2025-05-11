import React, { useEffect, useState } from "react";
import axios from "axios";

function OrderList() {
  const [orders, setOrders] = useState([]);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [month, setMonth] = useState("");

  const fetchOrders = (filters = {}) => {
    let url = "https://restaurant-backend-v.up.railway.app/api/orders/?";
    if (filters.startDate) url += `start_date=${filters.startDate}&`;
    if (filters.endDate) url += `end_date=${filters.endDate}&`;
    if (filters.month) url += `month=${filters.month}&`;

    axios
      .get(url)
      .then((res) => setOrders(res.data))
      .catch((err) => console.error("Lỗi khi lấy danh sách đơn hàng:", err));
  };

  useEffect(() => {
    fetchOrders(); // Lấy tất cả đơn hàng khi load trang
  }, []);

  const handleOrderClick = (orderId) => {
    axios
      .get(`https://restaurant-backend-v.up.railway.app/api/orders/${orderId}/`)
      .then((res) => setSelectedOrder(res.data))
      .catch((err) => console.error("Lỗi khi lấy chi tiết đơn hàng:", err));
  };

  return (
    <div>
      <h1>📋 Danh sách đơn hàng</h1>

      {/* Bộ lọc */}
      <div>
        <label>
          Từ ngày:
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </label>
        <label>
          Đến ngày:
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </label>
        <label>
          Tháng:
          <select value={month} onChange={(e) => setMonth(e.target.value)}>
            <option value="">--Chọn tháng--</option>
            {[...Array(12)].map((_, i) => (
              <option key={i + 1} value={i + 1}>
                {i + 1}
              </option>
            ))}
          </select>
        </label>
        <button onClick={() => fetchOrders({ startDate, endDate, month })}>
          Lọc
        </button>
      </div>

      {/* Bảng danh sách đơn hàng */}
      <table border="1">
        <thead>
          <tr>
            <th>Order ID</th>
            <th>Bàn</th>
            <th>Ngày tạo</th>
            <th>Trạng thái</th>
            <th>Đã thanh toán</th>
            <th>Tổng tiền</th>
            <th>Chi tiết</th>
          </tr>
        </thead>
        <tbody>
          {orders.map((order) => (
            <tr key={order.id}>
              <td>{order.id}</td>
              <td>{order.table_number}</td>
              <td>{new Date(order.created_at).toLocaleString()}</td>
              <td>{order.status}</td>
              <td>{order.is_paid ? "✅" : "❌"}</td>
              <td>${order.total_price.toFixed(2)}</td>
              <td>
                <button onClick={() => handleOrderClick(order.id)}>Xem</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Chi tiết đơn hàng */}
      {selectedOrder && (
        <div>
          <h2>Chi tiết đơn hàng #{selectedOrder.id}</h2>
          <p>Bàn: {selectedOrder.table_number}</p>
          <p>Ngày tạo: {new Date(selectedOrder.created_at).toLocaleString()}</p>
          <p>Trạng thái: {selectedOrder.status}</p>
          <p>Đã thanh toán: {selectedOrder.is_paid ? "✅" : "❌"}</p>
          <p>Tổng tiền: ${selectedOrder.total_price.toFixed(2)}</p>
          <h3>Danh sách món:</h3>
          <ul>
            {selectedOrder.items.map((item, index) => (
              <li key={index}>
                {item.item_name} x {item.quantity} = $
                {(item.item_price * item.quantity).toFixed(2)}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default OrderList;
