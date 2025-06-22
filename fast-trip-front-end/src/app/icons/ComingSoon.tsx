import { IIconProps } from "@/app/types/generic";

const ComingSoon = ({ height, width, fill, style }: IIconProps) => (
  <svg
    width={width || "120"}
    height={height || "32"}
    viewBox="0 0 120 32"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    style={style}
  >
    <rect x="0.5" width="119" height="32" rx="16" fill="#EBF6F2" />
    <foreignObject x="0" y="0" width="120" height="32">
      <div
        // xmlns="http://www.w3.org/1999/xhtml"
        className="w-full h-full flex items-center justify-center text-[#0AA86F] font-bold text-sm"
      >
        Coming soon
      </div>
    </foreignObject>
  </svg>
);

export default ComingSoon;
