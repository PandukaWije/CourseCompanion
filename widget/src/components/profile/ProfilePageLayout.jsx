import React from "react";
import { ProfileHeader } from "./ProfileHeader";

/**
 * ProfilePageLayout Component
 * Layout for profile page with header and centered content
 */
export const ProfilePageLayout = () => {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100%",
        width: "100%",
        background: "#FFFFFF",
      }}
    >
      {/* Header */}
      <ProfileHeader />

      {/* Body - Centered Content */}
      <div
        style={{
          flex: 1,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: "40px 20px",
        }}
      >
        <p
          style={{
            fontSize: "18px",
            fontWeight: "500",
            color: "#374151",
            textAlign: "center",
          }}
        >
          Your profile
        </p>
      </div>
    </div>
  );
};

export default ProfilePageLayout;