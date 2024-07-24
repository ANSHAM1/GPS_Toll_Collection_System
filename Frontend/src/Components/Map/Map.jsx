import React from "react";
import styles from "./Map.module.css";

import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  useMap,
  GeoJSON,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";

import { useEffect } from "react";

const Map = ({ position,zoom, style, geoJSON }) => {
  return (
    <MapContainer
      className={styles.map}
      center={position}
      zoom={zoom || 13}
      style={style}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      {geoJSON && <GeoJSON data={geoJSON} />}
      {position && <MapUpdater position={position} />}
      <Marker position={position}>
        <Popup>
          Current Position: {position[0] + " " + position[1]} <br></br>{" "}
        </Popup>
      </Marker>
    </MapContainer>
  );
};

const MapUpdater = ({ position }) => {
  const map = useMap();

  useEffect(() => {
    map.setView(position);
  }, [position, map]);

  return null;
};

export default Map;
