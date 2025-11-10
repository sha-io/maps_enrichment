import { useRef, useEffect } from 'react';
import maplibregl, { Map as MapLibreMap } from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

export default function Map() {
  const mapRef = useRef<HTMLDivElement | null>(null);
  const mapInstance = useRef<MapLibreMap | null>(null);

  useEffect(() => {
    if (mapInstance.current) return; 
    
    if (!mapRef.current) return; 

    mapInstance.current = new maplibregl.Map({
      container: mapRef.current,
      style: 'https://demotiles.maplibre.org/style.json',
      center: [0, 0],
      zoom: 1,
    });

    mapInstance.current.addControl(new maplibregl.NavigationControl(), 'top-right');

    return () => {
      mapInstance.current?.remove();
      mapInstance.current = null;
    };
  }, []);

  return (
    <div
      ref={mapRef}
      id="map"
      style={{ height: '100vh', width: '100%' }}
    />
  );
}
