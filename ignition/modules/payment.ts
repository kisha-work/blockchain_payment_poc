import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

const PaymentModule = buildModule("PaymentModule", (m) => {
  const payment = m.contract("Payment");
  const token = m.contract("Token", ["PaymentToken", "PMT", 1000000]);

  return { payment, token };
});

export default PaymentModule;
