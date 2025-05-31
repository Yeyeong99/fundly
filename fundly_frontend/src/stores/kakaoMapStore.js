// src/stores/mapStore.js
import { defineStore } from 'pinia'

export const useMapStore = defineStore('map', {
  state: () => ({
    map: null,
    ps: null,
    infowindow: null,
    mapData: [],
    bankData: [],
    selectedDo: '',
    selectedSi: '',
    selectedBank: '',
  }),
  actions: {
    async initMap(mapContainerId) {
      if (!window.kakao) {
        await new Promise((resolve) => {
          const script = document.createElement('script')
          script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${import.meta.env.VITE_KAKAO_JS_ID}&libraries=services&autoload=false`
          script.onload = () => {
            window.kakao.maps.load(resolve)
          }
          document.head.appendChild(script)
        })
      } else {
        await new Promise((resolve) => {
          window.kakao.maps.load(resolve)
        })
      }

      const kakao = window.kakao
      const mapOption = {
        center: new kakao.maps.LatLng(37.4978, 127.02786),
        level: 4,
        mapTypeId: kakao.maps.MapTypeId.ROADMAP,
      }

      this.map = new kakao.maps.Map(document.getElementById(mapContainerId), mapOption)
      this.ps = new kakao.maps.services.Places()
      this.infowindow = new kakao.maps.InfoWindow({ zIndex: 1 })
    },

    async loadData() {
      const res = await fetch('/data.json')
      const data = await res.json()

      this.mapData = data.mapInfo
      this.bankData = data.bankInfo
    },

    async search() {
      const query = `${this.selectedDo} ${this.selectedSi} ${this.selectedBank}`
      this.ps.keywordSearch(query, (results, status) => {
        if (status === kakao.maps.services.Status.OK) {
          const bounds = new kakao.maps.LatLngBounds()
          results.forEach((place) => {
            const marker = new kakao.maps.Marker({
              map: this.map,
              position: new kakao.maps.LatLng(place.y, place.x),
            })
            kakao.maps.event.addListener(marker, 'click', () => {
              this.infowindow.setContent(
                `<div style="padding:5px; font-size:12px;">${place.place_name}</div>`,
              )
              this.infowindow.open(this.map, marker)
            })
            bounds.extend(new kakao.maps.LatLng(place.y, place.x))
          })
          this.map.setBounds(bounds)
        }
      })
    },

    // ✅ 현재 위치 가져오기 액션 추가
    getCurrentLocation() {
      if (!this.map) {
        console.warn('지도가 아직 초기화되지 않았습니다.')
        return
      }

      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const lat = position.coords.latitude
            const lng = position.coords.longitude
            const locPosition = new kakao.maps.LatLng(lat, lng)

            // 마커 표시
            new kakao.maps.Marker({
              map: this.map,
              position: locPosition,
            })

            // 지도 중심 이동
            this.map.setCenter(locPosition)
            const geocoder = new kakao.maps.services.Geocoder()
            geocoder.coord2RegionCode(lng, lat, async (result, status) => {
              if (status === kakao.maps.services.Status.OK && result.length > 0) {
                const region = result[0]
                this.selectedDo = region.region_1depth_name
                this.selectedSi = region.region_2depth_name

                // 은행명이 선택된 경우에만 자동 검색 실행
                if (this.selectedBank) {
                  await this.search()
                }
              }
            })
          },
          (error) => {
            console.error('위치 정보를 가져오는 데 실패했습니다:', error)
          },
        )
      } else {
        console.warn('이 브라우저에서는 위치 정보가 지원되지 않습니다.')
      }
    },
  },
})
