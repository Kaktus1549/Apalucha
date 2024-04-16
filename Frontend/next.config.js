/**@type {import('next').NextConfig} */

const { hostname } = require('os')

let path = process.env.URL + '/api/:path'

module.exports = {
    async rewrites() {
      return [
        {
          source: '/api/:path',
          destination: path
        }
      ]
    },
    images: {
      remotePatterns:[
        {
          protocol: 'https',
          hostname: 'http.cat'
        }
      ]
    }
}