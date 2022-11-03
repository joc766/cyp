

const GET = (url, options={}) => {
    base_options = {
        method: "GET"
    }
    request_options = {
        ...base_options,
        ...options
    }
    response = fetch(url, request_options)
    return response
}
