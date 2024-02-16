/**@type {import('next').NextConfig} */

let path = process.env.URL + '/api/:path'

module.exports = {
    async rewrites() {
      return [
        {
          source: '/api/:path',
          destination: path
        }
      ]
    }
}

