// 处理编辑按钮点击的函数
  var responseDataDiv = document.getElementById('response-data');
  function handleEditBtnClick(event) {
    var propertyRow = event.target.closest('tr');
    var propertyId = propertyRow.getAttribute('data-id');
    var propertyName = propertyRow.children[0].textContent;
    var propertyType = propertyRow.children[1].textContent;
    var propertyValue = propertyRow.children[2].textContent;
    var propertyUnit = propertyRow.children[3].textContent;

    document.getElementById('propertyId').value = propertyId;
    document.getElementById('propertyName').value = propertyName;
    document.getElementById('propertyType').value = propertyType;
    document.getElementById('propertyValue').value = propertyValue;
    document.getElementById('propertyUnit').value = propertyUnit;

    responseDataDiv.innerText = '';
    document.getElementById('editForm').style.display = 'block';
  }

  // 处理删除按钮点击的函数
  function handleDeleteBtnClick(event) {
    var propertyRow = event.target.closest('tr');
    var propertyId = propertyRow.getAttribute('propertyId');

    // 执行 AJAX 请求以删除具有 propertyId 的属性
    // 如果成功，从表格中移除 propertyRow
  }

  // 处理添加新属性按钮点击的函数
  function handleAddPropertyBtnClick() {
    document.getElementById('propertyId').value = '';
    document.getElementById('propertyName').value = '';
    document.getElementById('propertyType').value = '';
    document.getElementById('propertyValue').value = '';
    document.getElementById('propertyUnit').value = '';

    document.getElementById('editForm').style.display = 'block';
  }

  // 处理取消按钮点击的函数
  function handleCancelBtnClick() {
    document.getElementById('editForm').style.display = 'none';
  }

  // 处理保存按钮点击的函数
  function handleSaveBtnClick() {
    var propertyId = document.getElementById('propertyId').value;
    var propertyName = document.getElementById('propertyName').value;
    var propertyType = document.getElementById('propertyType').value;
    var propertyValue = document.getElementById('propertyValue').value;
    var propertyUnit = document.getElementById('propertyUnit').value;


    // 执行 AJAX 请求以保存或更新属性数据
    var data = {
      property_id: propertyId,
      name: propertyName,
      type: propertyType,
      value: propertyValue,
      unit: propertyUnit
    };
  
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/edit_property', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function () {
        if (xhr.status === 200) {
            responseDataDiv.innerText = '保存成功';
        } else if (xhr.status === 400) {
            var response = JSON.parse(xhr.responseText);
            responseDataDiv.innerText = '保存失败: ' + response.error;
        } else {
            responseDataDiv.innerText = '通讯出错: ' + xhr.statusText;
        }
    };
    xhr.send(JSON.stringify(data));
  }
  

  // 附加事件监听器
  document.querySelectorAll('.editBtn').forEach(btn => {
    btn.addEventListener('click', handleEditBtnClick);
  });

  document.querySelectorAll('.deleteBtn').forEach(btn => {
    btn.addEventListener('click', handleDeleteBtnClick);
  });

  document.getElementById('addPropertyBtn').addEventListener('click', handleAddPropertyBtnClick);
  document.getElementById('cancelBtn').addEventListener('click', handleCancelBtnClick);
  document.getElementById('saveBtn').addEventListener('click', handleSaveBtnClick);

  // 在单击关闭按钮时关闭编辑表单
  document.querySelector('.close').addEventListener('click', function() {
    document.getElementById('editForm').style.display = 'none';
  });

  // 在单击编辑表单外部时关闭编辑表单
  window.addEventListener('click', function(event) {
    if (event.target == document.getElementById('editForm')) {
      document.getElementById('editForm').style.display = 'none';
    }
  });