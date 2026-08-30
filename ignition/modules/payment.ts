import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

const PaymentModule = buildModule("PaymentModule", (m) => {
  const payment = m.contract("Payment");

  return { payment };
});

export default PaymentModule;
