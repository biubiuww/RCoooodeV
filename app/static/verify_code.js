document.getElementById('verify-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var code = document.getElementById('code').value;
    var resultElement = document.getElementById('result');
    
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/verify', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                var data = JSON.parse(xhr.responseText);
                var valid = data.valid;
                var message = data.message;
                var expirationDate = data.expiration_date || '';
                var maxUsage = data.max_usage || '';
                var usageCount = data.usage_count || '';
                
                var resultString = '';
                if (valid) {
                    resultString += '注册码有效<br>';
                    if (expirationDate) {
                        // 时间类型的注册码
                        var expirationDateFormatted = new Date(expirationDate);
                        var formattedDateString = expirationDateFormatted.getFullYear() + '/' +
                            ('0' + (expirationDateFormatted.getMonth() + 1)).slice(-2) + '/' +
                            ('0' + expirationDateFormatted.getDate()).slice(-2) + ' ' +
                            ('0' + expirationDateFormatted.getHours()).slice(-2) + ':' +
                            ('0' + expirationDateFormatted.getMinutes()).slice(-2) + ':' +
                            ('0' + expirationDateFormatted.getSeconds()).slice(-2);
                    
                        resultString += '过期时间: ' + formattedDateString + '<br>';
                        var currentDate = new Date();
                        var remainingTime = new Date(expirationDate) - currentDate;
                        var days = Math.floor(remainingTime / (1000 * 60 * 60 * 24));
                        var hours = Math.floor((remainingTime % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                        var minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
                        var seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);
                        resultString += '剩余到期时间: ' + days + '天 ' + hours + '小时 ' + minutes + '分钟 ' + seconds + '秒<br>';
                    }
                    if (maxUsage !== '') {
                        // 次数类型的注册码
                        resultString += '总使用次数: ' + maxUsage + '<br>';
                        if (usageCount !== '') {
                            resultString += '已使用次数: ' + usageCount + '<br>';
                            var remainingUsages = maxUsage - usageCount;
                            resultString += '剩余可用次数: ' + remainingUsages + '<br>';
                        }
                    }
                } else {
                    resultString += message + '<br>';
                }
                resultElement.innerHTML = resultString;
            } else {
                console.error('Error:', xhr.statusText);
                resultElement.innerText = '验证注册码时发生错误';
            }
        }
    };
    xhr.send(JSON.stringify({ code: code }));
    
});
