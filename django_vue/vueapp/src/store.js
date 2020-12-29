import Vue from 'vue'
import Vuex from 'vuex'
import { getAPI } from './axios-api'

Vue.use(Vuex)
export default new Vuex.Store({
    state: {
        accessToken: null,
        refreshToken: null,
    },
    mutations: {
        updateStorage (state, { access, refresh}){
            state.accessToken = access
            state.refreshToken = refresh
        }
    },
    actions: {
        userLogin (context, usercredentials){
          return new Promise((resolve) => {
              getAPI.post('/api-token/', {
                  email: usercredentials.username,
                  password: usercredentials.password
              })
              .then(response => {
                  context.commit('updateStorage',{
                      access: response.data.access,
                      refresh: response.data.refresh
                    })
                    resolve()
              })
          })  
        }
    }
})