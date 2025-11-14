import { MapContextWrapper } from './context/MapContext/MapContext'
import './index.css'
import Map from './Map'
import Sidebar from './Sidebar'

export default function App() {
  const style = 'https://raw.githubusercontent.com/go2garret/maps/main/src/assets/json/openStreetMap.json';
  const focus: [number, number] = [0.1276, 51.5072]
  const zoom = 5
  return (
    <MapContextWrapper id='map' center={focus} style={style} zoom={zoom}>
      <div className='flex flex-row-reverse'>
        <Sidebar />
        <Map />
      </div>
    </MapContextWrapper>
  )
}
