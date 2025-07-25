import { IIconProps } from "@/app/types/generic";

const Warehouse = ({ height, width, fill, style }: IIconProps) => (
  <svg
    width={width || "32"}
    height={height || "32"}
    viewBox="0 0 32 32"
    fill={fill || "none"}
    xmlns="http://www.w3.org/2000/svg"
    style={style}
  >
    <rect
      width={width || "32"}
      height={height || "32"}
      rx="8"
      fill={fill || "#0AA86F"}
    />
    <path
      d="M7.6665 23.5V8.5H15.9998V11.8333H24.3332V23.5H7.6665ZM9.33317 21.8333H10.9998V20.1667H9.33317V21.8333ZM9.33317 18.5H10.9998V16.8333H9.33317V18.5ZM9.33317 15.1667H10.9998V13.5H9.33317V15.1667ZM9.33317 11.8333H10.9998V10.1667H9.33317V11.8333ZM12.6665 21.8333H14.3332V20.1667H12.6665V21.8333ZM12.6665 18.5H14.3332V16.8333H12.6665V18.5ZM12.6665 15.1667H14.3332V13.5H12.6665V15.1667ZM12.6665 11.8333H14.3332V10.1667H12.6665V11.8333ZM15.9998 21.8333H22.6665V13.5H15.9998V15.1667H17.6665V16.8333H15.9998V18.5H17.6665V20.1667H15.9998V21.8333ZM19.3332 16.8333V15.1667H20.9998V16.8333H19.3332ZM19.3332 20.1667V18.5H20.9998V20.1667H19.3332Z"
      fill="white"
    />
  </svg>
);

export default Warehouse;
