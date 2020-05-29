import os
import json
import datetime
import pandas as pd
from app.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@csrf_exempt
def loginCheck(request):
    params = json.loads(request.body)
    user = User.objects.get(phone=params['phone'])
    if user.password == params['password']:
        return JsonResponse({'name': user.name, 'pwd': user.password, 'id': user.id, 'role': user.role.name})
    return JsonResponse({'res': 'fail'})


@csrf_exempt
def updatePwd(request):
    params = json.loads(request.body)
    user = User.objects.get(id=params['id'])
    user.password = params['password']
    user.save()
    return JsonResponse({'ok': 'ok'})


@csrf_exempt
def updateProject(request):
    params = json.loads(request.body)
    for uid in params['targetKeys']:
        user = User.objects.get(id=int(uid))
        user.projects.add(Project.objects.get(id=params['id']))
        user.save()
    return JsonResponse({'res': 'success'})


@csrf_exempt
def bomAna(request):
    path = BASE_DIR+'/static/check/'
    params = json.loads(request.body)
    baseMaterial = pd.read_excel(
        BASE_DIR+'/static/material.xlsx', header=1, usecols=[4, 5])

    baseChange = baseMaterial['*(物料)名称'].str.cat(
        baseMaterial['(物料)规格型号'], sep='/')

    sheets = pd.ExcelFile(path+params['name'])
    res, sheetList, total, hint = [], [], 0, ''

    for sheet in sheets.sheet_names:
        if params['model'] == '机械':
            if '机械' in params['name']:
                machineExcel = pd.read_excel(
                    path+params['name'], header=4, sheet_name=sheet,  usecols=[0, 1, 2, 6])
                machine = machineExcel[(machineExcel['类型'] == '市购件')
                                       | (machineExcel['类型'] == '标准件')]
                total = len(machine)+total
                for num, name, size in zip(machine['序号'], machine['图号/名称'], machine['名称/型号']):
                    if name+'/'+str(size) not in baseChange.values:
                        res.append({'sheet': sheet, 'num': num,
                                    'name': name, 'size': size})
            else:
                hint = '请上传格式正确的BOM'
        else:
            if '电气' in params['name']:
                electricExcel = pd.read_excel(
                    path+params['name'], header=4, sheet_name=sheet,  usecols=[0, 1, 2, 5])
                electric = electricExcel[(electricExcel['类型'] == '市购件')
                                         | (electricExcel['类型'] == '标准件')]
                total = len(electric)+total
                for num, name, size in zip(electric['名称'].index, electric['名称'], electric['型号']):
                    if name+'/'+str(size) not in baseChange.values:
                        res.append({'sheet': sheet, 'num': str(num+6),
                                    'name': name, 'size': size})
            else:
                hint = '请上传格式正确的BOM'

        sheetList.append({'sheet': sheet, 'data': list(
            filter(lambda obj: obj['sheet'] == sheet, res))})

    result = '总计匹配：%s个/问题项：%s个' % (total, len(res))
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    bom = BomAna()
    bom.result = result
    bom.target = params['name']
    bom.operator = params['name']
    bom.save()

    return JsonResponse({'name': params['name'], 'time': time, 'result': result, 'sheets': sheetList, 'hint': hint})


@csrf_exempt
def bomCheck(request):
    f = request.FILES['file']
    path = BASE_DIR+'/static/check/'
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path+'/'+f.name, 'wb') as uf:
        for chunk in f.chunks():
            uf.write(chunk)
    return JsonResponse({'res': 'success'})


@csrf_exempt
def getMaterials(request):
    try:
        name = ''
        res = pd.read_excel(BASE_DIR+'/static/material.xlsx',
                            usecols=[1, 2, 3, 4, 5, 6, 7])
        res.fillna('', inplace=True)
        with open(BASE_DIR+'/static/temp.txt', 'r') as f:
            name = f.readline()
        for f in os.listdir(BASE_DIR+'/static/check/'):
            os.remove(BASE_DIR+'/static/check/'+f)

        data = map(lambda obj: {'key': res.values.tolist().index(obj), 'FNumber': obj[0], 'FName': obj[1], 'FSpecification': obj[
            2], 'FDescription': obj[3], 'FMaterialGroup': obj[4], 'FBaseUnitId': obj[5], 'stock': obj[6]}, res.values.tolist())

        return JsonResponse({'res': list(data), 'time': '%s年%s月%s日%s点%s分%s秒' % (name[3:7], name[7:9], name[9:11], name[11:13], name[13:15], name[15:17])})
    except:
        return JsonResponse({'res': [], 'time': ''})


@csrf_exempt
def upload(request):
    f = request.FILES['file']
    upPath = BASE_DIR+'/static/appendix/%s' % datetime.datetime.now().strftime('%Y-%m-%d')
    if not os.path.exists(upPath):
        os.makedirs(upPath)
    with open(upPath+'/'+f.name, 'wb') as uf:
        for chunk in f.chunks():
            uf.write(chunk)
    return JsonResponse({'ok': 'ok'})


@csrf_exempt
def multUpload(request):
    f = request.FILES['file']

    upPath = BASE_DIR+'/static/material'
    if not os.path.exists(upPath):
        os.makedirs(upPath)

    if '物料' in f.name:
        with open(BASE_DIR+'/static/temp.txt', 'w') as tf:
            tf.write(f.name)
    res = ''
    with open(upPath+'/'+f.name, 'wb') as uf:
        for chunk in f.chunks():
            uf.write(chunk)
    return JsonResponse({'ok': 'ok'})


@csrf_exempt
def analyseMaterial(request):
    res = ''
    files = os.listdir(BASE_DIR+'/static/material')
    stock = pd.read_excel(
        BASE_DIR+'/static/material/'+files[0], usecols=[0, 5])
    stockDict = stock.groupby(['物料编码'])['库存量(主单位)'].sum()
    material = pd.read_excel(
        BASE_DIR+'/static/material/'+files[1], header=1, usecols=[5, 6, 8, 11, 13, 28])
    material = material.dropna(axis=0, how='all')

    for i in material.index:
        try:
            material.loc[i, 'stock'] = stockDict[material.loc[i]['(物料)编码']]
        except:
            material.loc[i, 'stock'] = ''
    material.to_excel(BASE_DIR+'/static/material.xlsx')
    for f in files:
        os.remove(BASE_DIR+'/static/material/'+f)
    res = 'success'
    return JsonResponse({'res': res})


@csrf_exempt
def exportData(request):

    def problemStatus(status):
        if status == '1':
            return '待解决'
        if status == '2':
            return '处理中'
        if status == '3':
            return '已解决'

    def projectStatus(status):
        if status == '1':
            return '进行中'
        if status == '2':
            return '已完成'

    def persons(persons):
        res = ''
        for person in persons:
            res += '%s,' % person['name']
        return res

    def progresses(progresses):
        res = ''
        for progress in progresses:
            res += '创建人:%s,创建时间:%s,进度描述:%s;\r\n' % (
                progress['creator'], progress['time'], progress['description'])
        return res

    def sections(sections):
        res = ''
        for section in sections:
            res += '节点名称:%s,节点时间:%s,节点描述:%s;\r\n' % (
                section['name'], section['time'], section['description'])
        return res

    params = json.loads(request.body)
    if params['model'] == 'user' or params['model'] == 'problem':
        data = []
        problems = Problem.objects.all()
        for problem in problems:
            data.append({'问题编号': problem.number, '问题主题': problem.theme, '发起人': problem.promoter, '接收人': problem.receiver, '抄送人': problem.carbonCopy, '创建时间': problem.createTime,
                         '期望回复时间': problem.expectTime, 'endTime': problem.endTime, '问题状态': problemStatus(problem.status), '问题描述': problem.description, '发起人意见': problem.promAdvice, '接收人意见': problem.receAdvice})
        df = pd.DataFrame(data)
        df.to_excel(BASE_DIR+'/static/问题列表.xlsx')
    if params['model'] == 'project':
        data = []
        projects = Project.objects.all()
        for project in projects:
            data.append({'项目名称': project.name, '项目状态': projectStatus(project.status), '项目甲方': project.owner,
                         '开始时间': project.startTime, '结束时间': project.endTime, '项目编号': project.number, '项目节点': sections(project.sections.all().values()), '项目进度': progresses(project.progresses.all().values()), '相关人员': persons(project.persons.all().values())})
        df = pd.DataFrame(data)
        df.to_excel(BASE_DIR+'/static/项目列表.xlsx')
    return JsonResponse({'ok': 'ok'})
