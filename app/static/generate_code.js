document.addEventListener('DOMContentLoaded', function () {
    var codeTypeSelect = document.getElementById('code_type');
    var expirationDurationDiv = document.getElementById('expiration_duration_div');
    var maxUsageDiv = document.getElementById('max_usage_div');
    var expirationDateResult = document.getElementById('expiration_date_result');
    var responseDataDiv = document.getElementById('response-data'); // 新添加的 <div> 元素用于显示来自后端的数据

    // 计算过期时间
    function calculateExpirationDate() {
        var duration = parseInt(document.getElementById('expiration_duration').value);
        var unit = document.getElementById('duration_unit').value;
        var currentDate = new Date();

        switch (unit) {
            case 'days':
                currentDate.setDate(currentDate.getDate() + duration);
                break;
            case 'weeks':
                currentDate.setDate(currentDate.getDate() + duration * 7);
                break;
            case 'months':
                currentDate.setMonth(currentDate.getMonth() + duration);
                break;
        }

        // 删除毫秒部分
        currentDate.setMilliseconds(0);

        // 将过期日期转换为本地时间字符串
        var expirationDateString = currentDate.toLocaleString();
        expirationDateResult.innerText = '过期时间: ' + expirationDateString;


        return currentDate.toISOString(); // 返回计算的过期时间
    }

    // 根据注册码类型显示相应的输入框
    function showInputFields() {
        var codeType = codeTypeSelect.value;
        if (codeType === 'time') {
            expirationDurationDiv.style.display = 'block';
            maxUsageDiv.style.display = 'none';
            document.getElementById('expiration_duration').setAttribute('required', true); // 设置过期时间为必填
            document.getElementById('max_usage').removeAttribute('required'); // 移除最大使用量的必填属性
        } else if (codeType === 'usage') {
            expirationDurationDiv.style.display = 'none';
            maxUsageDiv.style.display = 'block';
            document.getElementById('expiration_duration').removeAttribute('required'); // 移除过期时间的必填属性
            document.getElementById('max_usage').setAttribute('required', true); // 设置最大使用量为必填
        }
    }

    // 初始化显示对应的输入框
    showInputFields();

    // code类型选择的事件监听器
    codeTypeSelect.addEventListener('change', function () {
        showInputFields(); // 根据选择的注册码类型显示相应的输入框
        expirationDateResult.innerText = ''; // 切换类型时隐藏注册信息消息
        responseDataDiv.innerText = ''; // 切换类型时隐藏注册信息消息
    });

    // 过期时间输入框的事件监听器
    document.getElementById('expiration_duration').addEventListener('input', function () {
        calculateExpirationDate();
        responseDataDiv.innerText = ''; // 输入事件发生时隐藏注册信息消息
    });

    // 表单提交事件监听器
    document.getElementById('generate-form').addEventListener('submit', function (event) {
        event.preventDefault(); // 阻止默认表单提交行为

        var codeType = document.getElementById('code_type').value;
        var data = {};

        if (codeType === 'time') {
            data.code_type = codeType;
            data.expiration_date = calculateExpirationDate();
        } else if (codeType === 'usage') {
            data.code_type = codeType;
            var maxUsageValue = document.getElementById('max_usage').value.trim(); // 去除输入值两端的空格
            if (maxUsageValue !== '') {
                // 如果最大使用量输入框有值，则将其包含在数据中
                data.max_usage = parseInt(maxUsageValue);
            }
        }

        // 发送到后端的 AJAX POST 请求
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/generate_code', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function () {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.code) {
                    // 如果返回的注册信息中包含注册码，则显示在网页中
                    responseDataDiv.innerText = 'Registration Code: ' + response.code;
                    document.getElementById('generate-form').reset(); // 表单提交后重置表单
                    showInputFields(); // 根据返回数据重新显示对应的输入框
                } else {
                    console.error('未收到有效的注册信息。');
                }
            } else {
                console.error('生成注册码出错:', xhr.statusText);
            }
        };
        xhr.onerror = function () {
            console.error('生成注册码时发生网络错误。');
        };
        xhr.send(JSON.stringify(data));
    });
});
