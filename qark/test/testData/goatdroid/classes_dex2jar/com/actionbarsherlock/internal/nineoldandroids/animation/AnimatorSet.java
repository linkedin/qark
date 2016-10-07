package com.actionbarsherlock.internal.nineoldandroids.animation;

import android.view.animation.Interpolator;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;

public final class AnimatorSet
  extends Animator
{
  private ValueAnimator mDelayAnim = null;
  private long mDuration = -1L;
  private boolean mNeedsSort = true;
  private HashMap<Animator, Node> mNodeMap = new HashMap();
  private ArrayList<Node> mNodes = new ArrayList();
  private ArrayList<Animator> mPlayingSet = new ArrayList();
  private AnimatorSetListener mSetListener = null;
  private ArrayList<Node> mSortedNodes = new ArrayList();
  private long mStartDelay = 0L;
  private boolean mStarted = false;
  boolean mTerminated = false;
  
  public AnimatorSet() {}
  
  private void sortNodes()
  {
    if (this.mNeedsSort)
    {
      this.mSortedNodes.clear();
      ArrayList localArrayList1 = new ArrayList();
      int n = this.mNodes.size();
      int i1 = 0;
      ArrayList localArrayList2;
      if (i1 >= n) {
        localArrayList2 = new ArrayList();
      }
      int i3;
      for (;;)
      {
        if (localArrayList1.size() <= 0)
        {
          this.mNeedsSort = false;
          if (this.mSortedNodes.size() == this.mNodes.size()) {
            break label298;
          }
          throw new IllegalStateException("Circular dependencies cannot exist in AnimatorSet");
          Node localNode4 = (Node)this.mNodes.get(i1);
          if ((localNode4.dependencies == null) || (localNode4.dependencies.size() == 0)) {
            localArrayList1.add(localNode4);
          }
          i1++;
          break;
        }
        int i2 = localArrayList1.size();
        i3 = 0;
        if (i3 < i2) {
          break label176;
        }
        localArrayList1.clear();
        localArrayList1.addAll(localArrayList2);
        localArrayList2.clear();
      }
      label176:
      Node localNode2 = (Node)localArrayList1.get(i3);
      this.mSortedNodes.add(localNode2);
      int i4;
      if (localNode2.nodeDependents != null) {
        i4 = localNode2.nodeDependents.size();
      }
      for (int i5 = 0;; i5++)
      {
        if (i5 >= i4)
        {
          i3++;
          break;
        }
        Node localNode3 = (Node)localNode2.nodeDependents.get(i5);
        localNode3.nodeDependencies.remove(localNode2);
        if (localNode3.nodeDependencies.size() == 0) {
          localArrayList2.add(localNode3);
        }
      }
    }
    int i = this.mNodes.size();
    int j = 0;
    if (j >= i) {
      label298:
      return;
    }
    Node localNode1 = (Node)this.mNodes.get(j);
    int k;
    if ((localNode1.dependencies != null) && (localNode1.dependencies.size() > 0)) {
      k = localNode1.dependencies.size();
    }
    for (int m = 0;; m++)
    {
      if (m >= k)
      {
        localNode1.done = false;
        j++;
        break;
      }
      Dependency localDependency = (Dependency)localNode1.dependencies.get(m);
      if (localNode1.nodeDependencies == null) {
        localNode1.nodeDependencies = new ArrayList();
      }
      if (!localNode1.nodeDependencies.contains(localDependency.node)) {
        localNode1.nodeDependencies.add(localDependency.node);
      }
    }
  }
  
  public void cancel()
  {
    this.mTerminated = true;
    Iterator localIterator3;
    label74:
    Iterator localIterator2;
    if (isStarted())
    {
      ArrayList localArrayList1 = this.mListeners;
      ArrayList localArrayList2 = null;
      if (localArrayList1 != null)
      {
        localArrayList2 = (ArrayList)this.mListeners.clone();
        localIterator3 = localArrayList2.iterator();
        if (localIterator3.hasNext()) {
          break label100;
        }
      }
      if ((this.mDelayAnim == null) || (!this.mDelayAnim.isRunning())) {
        break label119;
      }
      this.mDelayAnim.cancel();
      if (localArrayList2 != null) {
        localIterator2 = localArrayList2.iterator();
      }
    }
    for (;;)
    {
      if (!localIterator2.hasNext())
      {
        this.mStarted = false;
        return;
        label100:
        ((Animator.AnimatorListener)localIterator3.next()).onAnimationCancel(this);
        break;
        label119:
        if (this.mSortedNodes.size() <= 0) {
          break label74;
        }
        Iterator localIterator1 = this.mSortedNodes.iterator();
        while (localIterator1.hasNext()) {
          ((Node)localIterator1.next()).animation.cancel();
        }
        break label74;
      }
      ((Animator.AnimatorListener)localIterator2.next()).onAnimationEnd(this);
    }
  }
  
  public AnimatorSet clone()
  {
    AnimatorSet localAnimatorSet = (AnimatorSet)super.clone();
    localAnimatorSet.mNeedsSort = true;
    localAnimatorSet.mTerminated = false;
    localAnimatorSet.mStarted = false;
    localAnimatorSet.mPlayingSet = new ArrayList();
    localAnimatorSet.mNodeMap = new HashMap();
    localAnimatorSet.mNodes = new ArrayList();
    localAnimatorSet.mSortedNodes = new ArrayList();
    HashMap localHashMap = new HashMap();
    Iterator localIterator1 = this.mNodes.iterator();
    Iterator localIterator4;
    if (!localIterator1.hasNext()) {
      localIterator4 = this.mNodes.iterator();
    }
    for (;;)
    {
      if (!localIterator4.hasNext())
      {
        return localAnimatorSet;
        Node localNode1 = (Node)localIterator1.next();
        Node localNode2 = localNode1.clone();
        localHashMap.put(localNode1, localNode2);
        localAnimatorSet.mNodes.add(localNode2);
        localAnimatorSet.mNodeMap.put(localNode2.animation, localNode2);
        localNode2.dependencies = null;
        localNode2.tmpDependencies = null;
        localNode2.nodeDependents = null;
        localNode2.nodeDependencies = null;
        ArrayList localArrayList1 = localNode2.animation.getListeners();
        if (localArrayList1 == null) {
          break;
        }
        ArrayList localArrayList2 = null;
        Iterator localIterator2 = localArrayList1.iterator();
        for (;;)
        {
          if (!localIterator2.hasNext())
          {
            if (localArrayList2 == null) {
              break;
            }
            Iterator localIterator3 = localArrayList2.iterator();
            while (localIterator3.hasNext()) {
              localArrayList1.remove((Animator.AnimatorListener)localIterator3.next());
            }
            break;
          }
          Animator.AnimatorListener localAnimatorListener = (Animator.AnimatorListener)localIterator2.next();
          if ((localAnimatorListener instanceof AnimatorSetListener))
          {
            if (localArrayList2 == null) {
              localArrayList2 = new ArrayList();
            }
            localArrayList2.add(localAnimatorListener);
          }
        }
      }
      Node localNode3 = (Node)localIterator4.next();
      Node localNode4 = (Node)localHashMap.get(localNode3);
      if (localNode3.dependencies != null)
      {
        Iterator localIterator5 = localNode3.dependencies.iterator();
        while (localIterator5.hasNext())
        {
          Dependency localDependency = (Dependency)localIterator5.next();
          localNode4.addDependency(new Dependency((Node)localHashMap.get(localDependency.node), localDependency.rule));
        }
      }
    }
  }
  
  public void end()
  {
    this.mTerminated = true;
    Iterator localIterator3;
    Iterator localIterator2;
    label82:
    Iterator localIterator1;
    if (isStarted())
    {
      if (this.mSortedNodes.size() != this.mNodes.size())
      {
        sortNodes();
        localIterator3 = this.mSortedNodes.iterator();
        if (localIterator3.hasNext()) {
          break label127;
        }
      }
      if (this.mDelayAnim != null) {
        this.mDelayAnim.cancel();
      }
      if (this.mSortedNodes.size() > 0)
      {
        localIterator2 = this.mSortedNodes.iterator();
        if (localIterator2.hasNext()) {
          break label173;
        }
      }
      if (this.mListeners != null) {
        localIterator1 = ((ArrayList)this.mListeners.clone()).iterator();
      }
    }
    for (;;)
    {
      if (!localIterator1.hasNext())
      {
        this.mStarted = false;
        return;
        label127:
        Node localNode = (Node)localIterator3.next();
        if (this.mSetListener == null) {
          this.mSetListener = new AnimatorSetListener(this);
        }
        localNode.animation.addListener(this.mSetListener);
        break;
        label173:
        ((Node)localIterator2.next()).animation.end();
        break label82;
      }
      ((Animator.AnimatorListener)localIterator1.next()).onAnimationEnd(this);
    }
  }
  
  public ArrayList<Animator> getChildAnimations()
  {
    ArrayList localArrayList = new ArrayList();
    Iterator localIterator = this.mNodes.iterator();
    for (;;)
    {
      if (!localIterator.hasNext()) {
        return localArrayList;
      }
      localArrayList.add(((Node)localIterator.next()).animation);
    }
  }
  
  public long getDuration()
  {
    return this.mDuration;
  }
  
  public long getStartDelay()
  {
    return this.mStartDelay;
  }
  
  public boolean isRunning()
  {
    Iterator localIterator = this.mNodes.iterator();
    do
    {
      if (!localIterator.hasNext()) {
        return false;
      }
    } while (!((Node)localIterator.next()).animation.isRunning());
    return true;
  }
  
  public boolean isStarted()
  {
    return this.mStarted;
  }
  
  public Builder play(Animator paramAnimator)
  {
    if (paramAnimator != null)
    {
      this.mNeedsSort = true;
      return new Builder(paramAnimator);
    }
    return null;
  }
  
  public void playSequentially(List<Animator> paramList)
  {
    if ((paramList != null) && (paramList.size() > 0))
    {
      this.mNeedsSort = true;
      if (paramList.size() != 1) {
        break label44;
      }
      play((Animator)paramList.get(0));
    }
    for (;;)
    {
      return;
      label44:
      for (int i = 0; i < -1 + paramList.size(); i++) {
        play((Animator)paramList.get(i)).before((Animator)paramList.get(i + 1));
      }
    }
  }
  
  public void playSequentially(Animator... paramVarArgs)
  {
    if (paramVarArgs != null)
    {
      this.mNeedsSort = true;
      if (paramVarArgs.length != 1) {
        break label24;
      }
      play(paramVarArgs[0]);
    }
    for (;;)
    {
      return;
      label24:
      for (int i = 0; i < -1 + paramVarArgs.length; i++) {
        play(paramVarArgs[i]).before(paramVarArgs[(i + 1)]);
      }
    }
  }
  
  public void playTogether(Collection<Animator> paramCollection)
  {
    Builder localBuilder;
    Iterator localIterator;
    if ((paramCollection != null) && (paramCollection.size() > 0))
    {
      this.mNeedsSort = true;
      localBuilder = null;
      localIterator = paramCollection.iterator();
    }
    for (;;)
    {
      if (!localIterator.hasNext()) {
        return;
      }
      Animator localAnimator = (Animator)localIterator.next();
      if (localBuilder == null) {
        localBuilder = play(localAnimator);
      } else {
        localBuilder.with(localAnimator);
      }
    }
  }
  
  public void playTogether(Animator... paramVarArgs)
  {
    Builder localBuilder;
    if (paramVarArgs != null)
    {
      this.mNeedsSort = true;
      localBuilder = play(paramVarArgs[0]);
    }
    for (int i = 1;; i++)
    {
      if (i >= paramVarArgs.length) {
        return;
      }
      localBuilder.with(paramVarArgs[i]);
    }
  }
  
  public AnimatorSet setDuration(long paramLong)
  {
    if (paramLong < 0L) {
      throw new IllegalArgumentException("duration must be a value of zero or greater");
    }
    Iterator localIterator = this.mNodes.iterator();
    for (;;)
    {
      if (!localIterator.hasNext())
      {
        this.mDuration = paramLong;
        return this;
      }
      ((Node)localIterator.next()).animation.setDuration(paramLong);
    }
  }
  
  public void setInterpolator(Interpolator paramInterpolator)
  {
    Iterator localIterator = this.mNodes.iterator();
    for (;;)
    {
      if (!localIterator.hasNext()) {
        return;
      }
      ((Node)localIterator.next()).animation.setInterpolator(paramInterpolator);
    }
  }
  
  public void setStartDelay(long paramLong)
  {
    this.mStartDelay = paramLong;
  }
  
  public void setTarget(Object paramObject)
  {
    Iterator localIterator = this.mNodes.iterator();
    for (;;)
    {
      if (!localIterator.hasNext()) {
        return;
      }
      Animator localAnimator = ((Node)localIterator.next()).animation;
      if ((localAnimator instanceof AnimatorSet)) {
        ((AnimatorSet)localAnimator).setTarget(paramObject);
      } else if ((localAnimator instanceof ObjectAnimator)) {
        ((ObjectAnimator)localAnimator).setTarget(paramObject);
      }
    }
  }
  
  public void setupEndValues()
  {
    Iterator localIterator = this.mNodes.iterator();
    for (;;)
    {
      if (!localIterator.hasNext()) {
        return;
      }
      ((Node)localIterator.next()).animation.setupEndValues();
    }
  }
  
  public void setupStartValues()
  {
    Iterator localIterator = this.mNodes.iterator();
    for (;;)
    {
      if (!localIterator.hasNext()) {
        return;
      }
      ((Node)localIterator.next()).animation.setupStartValues();
    }
  }
  
  public void start()
  {
    this.mTerminated = false;
    this.mStarted = true;
    sortNodes();
    int i = this.mSortedNodes.size();
    int j = 0;
    final ArrayList localArrayList1;
    int k;
    label40:
    Iterator localIterator1;
    label61:
    label71:
    ArrayList localArrayList3;
    int i4;
    label100:
    ArrayList localArrayList2;
    int i1;
    if (j >= i)
    {
      localArrayList1 = new ArrayList();
      k = 0;
      if (k < i) {
        break label275;
      }
      if (this.mStartDelay > 0L) {
        break label475;
      }
      localIterator1 = localArrayList1.iterator();
      if (localIterator1.hasNext()) {
        break label439;
      }
      if (this.mListeners != null)
      {
        localArrayList3 = (ArrayList)this.mListeners.clone();
        int i3 = localArrayList3.size();
        i4 = 0;
        if (i4 < i3) {
          break label531;
        }
      }
      if ((this.mNodes.size() == 0) && (this.mStartDelay == 0L))
      {
        this.mStarted = false;
        if (this.mListeners != null)
        {
          localArrayList2 = (ArrayList)this.mListeners.clone();
          i1 = localArrayList2.size();
        }
      }
    }
    for (int i2 = 0;; i2++)
    {
      if (i2 >= i1)
      {
        return;
        Node localNode3 = (Node)this.mSortedNodes.get(j);
        ArrayList localArrayList4 = localNode3.animation.getListeners();
        Iterator localIterator2;
        if ((localArrayList4 != null) && (localArrayList4.size() > 0)) {
          localIterator2 = new ArrayList(localArrayList4).iterator();
        }
        for (;;)
        {
          if (!localIterator2.hasNext())
          {
            j++;
            break;
          }
          Animator.AnimatorListener localAnimatorListener = (Animator.AnimatorListener)localIterator2.next();
          if (((localAnimatorListener instanceof DependencyListener)) || ((localAnimatorListener instanceof AnimatorSetListener))) {
            localNode3.animation.removeListener(localAnimatorListener);
          }
        }
        label275:
        Node localNode1 = (Node)this.mSortedNodes.get(k);
        if (this.mSetListener == null) {
          this.mSetListener = new AnimatorSetListener(this);
        }
        if ((localNode1.dependencies == null) || (localNode1.dependencies.size() == 0))
        {
          localArrayList1.add(localNode1);
          localNode1.animation.addListener(this.mSetListener);
          k++;
          break label40;
        }
        int m = localNode1.dependencies.size();
        for (int n = 0;; n++)
        {
          if (n >= m)
          {
            localNode1.tmpDependencies = ((ArrayList)localNode1.dependencies.clone());
            break;
          }
          Dependency localDependency = (Dependency)localNode1.dependencies.get(n);
          localDependency.node.animation.addListener(new DependencyListener(this, localNode1, localDependency.rule));
        }
        label439:
        Node localNode2 = (Node)localIterator1.next();
        localNode2.animation.start();
        this.mPlayingSet.add(localNode2.animation);
        break label61;
        label475:
        this.mDelayAnim = ValueAnimator.ofFloat(new float[] { 0.0F, 1.0F });
        this.mDelayAnim.setDuration(this.mStartDelay);
        this.mDelayAnim.addListener(new AnimatorListenerAdapter()
        {
          boolean canceled = false;
          
          public void onAnimationCancel(Animator paramAnonymousAnimator)
          {
            this.canceled = true;
          }
          
          public void onAnimationEnd(Animator paramAnonymousAnimator)
          {
            int i;
            if (!this.canceled) {
              i = localArrayList1.size();
            }
            for (int j = 0;; j++)
            {
              if (j >= i) {
                return;
              }
              AnimatorSet.Node localNode = (AnimatorSet.Node)localArrayList1.get(j);
              localNode.animation.start();
              AnimatorSet.this.mPlayingSet.add(localNode.animation);
            }
          }
        });
        this.mDelayAnim.start();
        break label71;
        label531:
        ((Animator.AnimatorListener)localArrayList3.get(i4)).onAnimationStart(this);
        i4++;
        break label100;
      }
      ((Animator.AnimatorListener)localArrayList2.get(i2)).onAnimationEnd(this);
    }
  }
  
  private class AnimatorSetListener
    implements Animator.AnimatorListener
  {
    private AnimatorSet mAnimatorSet;
    
    AnimatorSetListener(AnimatorSet paramAnimatorSet)
    {
      this.mAnimatorSet = paramAnimatorSet;
    }
    
    public void onAnimationCancel(Animator paramAnimator)
    {
      int i;
      if ((!AnimatorSet.this.mTerminated) && (AnimatorSet.this.mPlayingSet.size() == 0) && (AnimatorSet.this.mListeners != null)) {
        i = AnimatorSet.this.mListeners.size();
      }
      for (int j = 0;; j++)
      {
        if (j >= i) {
          return;
        }
        ((Animator.AnimatorListener)AnimatorSet.this.mListeners.get(j)).onAnimationCancel(this.mAnimatorSet);
      }
    }
    
    public void onAnimationEnd(Animator paramAnimator)
    {
      paramAnimator.removeListener(this);
      AnimatorSet.this.mPlayingSet.remove(paramAnimator);
      ((AnimatorSet.Node)this.mAnimatorSet.mNodeMap.get(paramAnimator)).done = true;
      ArrayList localArrayList1;
      int i;
      int k;
      label72:
      ArrayList localArrayList2;
      int m;
      if (!AnimatorSet.this.mTerminated)
      {
        localArrayList1 = this.mAnimatorSet.mSortedNodes;
        i = 1;
        int j = localArrayList1.size();
        k = 0;
        if (k < j) {
          break label128;
        }
        if (i != 0) {
          if (AnimatorSet.this.mListeners != null)
          {
            localArrayList2 = (ArrayList)AnimatorSet.this.mListeners.clone();
            m = localArrayList2.size();
          }
        }
      }
      for (int n = 0;; n++)
      {
        if (n >= m)
        {
          this.mAnimatorSet.mStarted = false;
          return;
          label128:
          if (!((AnimatorSet.Node)localArrayList1.get(k)).done)
          {
            i = 0;
            break label72;
          }
          k++;
          break;
        }
        ((Animator.AnimatorListener)localArrayList2.get(n)).onAnimationEnd(this.mAnimatorSet);
      }
    }
    
    public void onAnimationRepeat(Animator paramAnimator) {}
    
    public void onAnimationStart(Animator paramAnimator) {}
  }
  
  public class Builder
  {
    private AnimatorSet.Node mCurrentNode;
    
    Builder(Animator paramAnimator)
    {
      this.mCurrentNode = ((AnimatorSet.Node)AnimatorSet.this.mNodeMap.get(paramAnimator));
      if (this.mCurrentNode == null)
      {
        this.mCurrentNode = new AnimatorSet.Node(paramAnimator);
        AnimatorSet.this.mNodeMap.put(paramAnimator, this.mCurrentNode);
        AnimatorSet.this.mNodes.add(this.mCurrentNode);
      }
    }
    
    public Builder after(long paramLong)
    {
      ValueAnimator localValueAnimator = ValueAnimator.ofFloat(new float[] { 0.0F, 1.0F });
      localValueAnimator.setDuration(paramLong);
      after(localValueAnimator);
      return this;
    }
    
    public Builder after(Animator paramAnimator)
    {
      AnimatorSet.Node localNode = (AnimatorSet.Node)AnimatorSet.this.mNodeMap.get(paramAnimator);
      if (localNode == null)
      {
        localNode = new AnimatorSet.Node(paramAnimator);
        AnimatorSet.this.mNodeMap.put(paramAnimator, localNode);
        AnimatorSet.this.mNodes.add(localNode);
      }
      AnimatorSet.Dependency localDependency = new AnimatorSet.Dependency(localNode, 1);
      this.mCurrentNode.addDependency(localDependency);
      return this;
    }
    
    public Builder before(Animator paramAnimator)
    {
      AnimatorSet.Node localNode = (AnimatorSet.Node)AnimatorSet.this.mNodeMap.get(paramAnimator);
      if (localNode == null)
      {
        localNode = new AnimatorSet.Node(paramAnimator);
        AnimatorSet.this.mNodeMap.put(paramAnimator, localNode);
        AnimatorSet.this.mNodes.add(localNode);
      }
      localNode.addDependency(new AnimatorSet.Dependency(this.mCurrentNode, 1));
      return this;
    }
    
    public Builder with(Animator paramAnimator)
    {
      AnimatorSet.Node localNode = (AnimatorSet.Node)AnimatorSet.this.mNodeMap.get(paramAnimator);
      if (localNode == null)
      {
        localNode = new AnimatorSet.Node(paramAnimator);
        AnimatorSet.this.mNodeMap.put(paramAnimator, localNode);
        AnimatorSet.this.mNodes.add(localNode);
      }
      localNode.addDependency(new AnimatorSet.Dependency(this.mCurrentNode, 0));
      return this;
    }
  }
  
  private static class Dependency
  {
    static final int AFTER = 1;
    static final int WITH;
    public AnimatorSet.Node node;
    public int rule;
    
    public Dependency(AnimatorSet.Node paramNode, int paramInt)
    {
      this.node = paramNode;
      this.rule = paramInt;
    }
  }
  
  private static class DependencyListener
    implements Animator.AnimatorListener
  {
    private AnimatorSet mAnimatorSet;
    private AnimatorSet.Node mNode;
    private int mRule;
    
    public DependencyListener(AnimatorSet paramAnimatorSet, AnimatorSet.Node paramNode, int paramInt)
    {
      this.mAnimatorSet = paramAnimatorSet;
      this.mNode = paramNode;
      this.mRule = paramInt;
    }
    
    private void startIfReady(Animator paramAnimator)
    {
      if (this.mAnimatorSet.mTerminated) {
        return;
      }
      int i = this.mNode.tmpDependencies.size();
      label139:
      for (int j = 0;; j++)
      {
        Object localObject = null;
        if (j >= i) {}
        for (;;)
        {
          this.mNode.tmpDependencies.remove(localObject);
          if (this.mNode.tmpDependencies.size() != 0) {
            break;
          }
          this.mNode.animation.start();
          this.mAnimatorSet.mPlayingSet.add(this.mNode.animation);
          return;
          AnimatorSet.Dependency localDependency = (AnimatorSet.Dependency)this.mNode.tmpDependencies.get(j);
          if ((localDependency.rule != this.mRule) || (localDependency.node.animation != paramAnimator)) {
            break label139;
          }
          localObject = localDependency;
          paramAnimator.removeListener(this);
        }
      }
    }
    
    public void onAnimationCancel(Animator paramAnimator) {}
    
    public void onAnimationEnd(Animator paramAnimator)
    {
      if (this.mRule == 1) {
        startIfReady(paramAnimator);
      }
    }
    
    public void onAnimationRepeat(Animator paramAnimator) {}
    
    public void onAnimationStart(Animator paramAnimator)
    {
      if (this.mRule == 0) {
        startIfReady(paramAnimator);
      }
    }
  }
  
  private static class Node
    implements Cloneable
  {
    public Animator animation;
    public ArrayList<AnimatorSet.Dependency> dependencies = null;
    public boolean done = false;
    public ArrayList<Node> nodeDependencies = null;
    public ArrayList<Node> nodeDependents = null;
    public ArrayList<AnimatorSet.Dependency> tmpDependencies = null;
    
    public Node(Animator paramAnimator)
    {
      this.animation = paramAnimator;
    }
    
    public void addDependency(AnimatorSet.Dependency paramDependency)
    {
      if (this.dependencies == null)
      {
        this.dependencies = new ArrayList();
        this.nodeDependencies = new ArrayList();
      }
      this.dependencies.add(paramDependency);
      if (!this.nodeDependencies.contains(paramDependency.node)) {
        this.nodeDependencies.add(paramDependency.node);
      }
      Node localNode = paramDependency.node;
      if (localNode.nodeDependents == null) {
        localNode.nodeDependents = new ArrayList();
      }
      localNode.nodeDependents.add(this);
    }
    
    public Node clone()
    {
      try
      {
        Node localNode = (Node)super.clone();
        localNode.animation = this.animation.clone();
        return localNode;
      }
      catch (CloneNotSupportedException localCloneNotSupportedException)
      {
        throw new AssertionError();
      }
    }
  }
}
